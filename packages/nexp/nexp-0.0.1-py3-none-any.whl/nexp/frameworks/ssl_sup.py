
import argparse
import logging

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchvision.datasets import CIFAR10
import torchvision.models
import torchvision.transforms as T

import nexp.models.vision as vision_models
from nexp.config import cifar10_path
import nexp.parser as nparser
from nexp.utils import set_all_seed
import nexp.datasets.datastats as datastats


logger = logging.getLogger("ssl")
logger.setLevel(logging.INFO)

logging.basicConfig(
    format="{asctime} {levelname} [{name:10s}:{lineno:3d}] {message}",
    style='{',
    datefmt='%H:%M:%S',
    level="INFO",
    handlers=[
        # Log to stderr, which is catched by SLURM into log files
        logging.StreamHandler(),
    ],
)

set_all_seed(0)


@torch.jit.script
def extract_labels_pairs(labels):
    n = len(labels)
    i = torch.zeros((n*(n-1))//2, dtype=torch.int64, device='cuda')
    j = torch.zeros((n*(n-1))//2, dtype=torch.int64, device='cuda')
    count = 0
    for k in range(n):
        for l in range(k+1, n):
            if labels[k] == labels[l]:
                i[count] = k
                j[count] = l
                count += 1
    return i[:count], j[:count]


logger.info("Parsing arguments")
parser = argparse.ArgumentParser(
    description="Training configuration",
) 
nparser.decorate_parser(parser)
config = parser.parse_args()
nparser.fill_namespace(config)


logger.info("Registering architecture")
model_name = config.architecture
tail, fan_in = vision_models.headless_model(model_name)
model_preprocessing = vision_models.model_preprocessing(model_name)

out_dim = config.output_dim
head = vision_models.ssl_head(fan_in, 4*out_dim, out_dim)
ssl_model = nn.Sequential(tail, head)

num_gpus = config.gpus_per_node * config.nodes
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

if num_gpus > 1:
    ssl_model = nn.DataParallel(ssl_model)
ssl_model.to(device)


logger.info("Registering dataset")
dataset_name = "cifar10"
mean, std = datastats.compute_mean_std(dataset_name, recompute=False)

transform = T.Compose(
    [T.ToTensor(), T.Normalize(mean=mean, std=std)]
)

trainset = torchvision.datasets.CIFAR10(
    root=cifar10_path, train=True, transform=transform
)
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=config.full_batch_size, shuffle=True, num_workers=config.cpus_per_task
)

logger.info("Solving pretext task")
optimizer = optim.AdamW(ssl_model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
lr_scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=config.epochs, eta_min=config.learning_rate / 50
)

for epoch in range(config.epochs):  # loop over the dataset multiple times
    
    I = torch.eye(out_dim, device=device, requires_grad=False)

    running_inv = 0.0
    running_reg = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        x, labels = data[0], data[1]
        x = x.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)
        ind_1, ind_2 = extract_labels_pairs(labels)

        # forward
        z = ssl_model(x)

        # orthogonal regularization
        reg = F.mse_loss(torch.cov(z.T), I)
        reg *= out_dim **2

        # invariance part
        inv = F.mse_loss(z[ind_1], z[ind_2])
        inv *= out_dim
        loss = .85 * inv + reg

        # backward loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        running_inv += inv.item()
        running_reg += reg.item()
        if i % 20 == 19:
            logger.info(f"Epoch: {epoch:3d} {i:3d}, Loss: {running_inv / 20}, {running_reg / 20}")
            running_inv = 0.0
            running_reg = 0.0

    if epoch % config.checkpoint_frequency == config.checkpoint_frequency - 1:
        state = {
            'arch': model_name,
            'state_dict': tail.state_dict(),
        }
        logger.info(f"saving model at epoch {epoch + 1}")
        torch.save(state, f"/checkpoint/vivc/nexp/pretrain_sup_{epoch}.pth")

logger.info('Finished Training upstream')


logger.info("Solving downstream task")
logger.info("Registering architecture")
tail.eval()
num_classes = 10
lin_head = nn.Linear(fan_in, num_classes, device=device)

logger.info("Registering optimizer")
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(lin_head.parameters(), lr=0.001, momentum=0.9)

for epoch in range(10 * config.epochs):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        x, labels = data[0], data[1]
        x = x.to(device)
        labels = labels.to(device)

        # forward
        if torch.no_grad():
            z = tail(x)
        loss = criterion(lin_head(z), labels)

        # backward loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    logger.info(f"Epoch: {epoch}, Loss: {running_loss / (i+1)}")

logger.info('Finished Training downstream')

logger.info("Evaluating model")
testset = torchvision.datasets.CIFAR10(
    root=cifar10_path, train=False, download=True, transform=transform
)
testloader = torch.utils.data.DataLoader(
    testset, batch_size=config.full_batch_size, shuffle=False, num_workers=config.cpus_per_task
)
model = nn.Sequential(tail, lin_head)
model.eval()

correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data[0].to(device), data[1].to(device)
        z = tail(images)
        outputs = lin_head(z)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

logger.info(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')
