"""
Train the model
"""

import argparse
import os
from torch.utils import data
from torch.utils.tensorboard import SummaryWriter
import torch
from utils import create_grids, write_to_tensorboard
import loss
from model import DeFINe
from loader import Dataset

parser = argparse.ArgumentParser(description="Path to face images and masks")
parser.add_argument('--img_path', help='path to image folder (up to images512x512)',
                    default='../dat/Faces/ffhq-dataset/images512x512/')
parser.add_argument('--mask_path', help='path to image folder (up to train or test)',
                    default='../dat/qd_imd/train/')
parser.add_argument('--checkpoint_path', help='path to store the checkpoints',
                    default='../dat/qd_imd/train/')
parser.add_argument('--batch_size', help='batch Size',
                    default=16)


args = parser.parse_args()
faces_path = args.img_path
mask_path = args.mask_path
checkpoint_path = args.checkpoint_path
batch_size = args.batch_size

use_cuda = torch.cuda.is_available()
cuda_device_count = torch.cuda.device_count()
print(f'Cuda Devices: {cuda_device_count}')
device = torch.device("cuda:0" if use_cuda else "cpu")

NET = DeFINe(device=device)

if cuda_device_count > 1:
    print("Use", cuda_device_count, "GPUs!")
    NET = torch.nn.DataParallel(NET)

NET.to(device)

params = {'batch_size': batch_size,
          'shuffle': True,
          'num_workers': 4}

max_epochs = 200

training_set = Dataset(faces_path=faces_path, mask_path=mask_path)
training_generator = data.DataLoader(training_set, **params)

validation_set = Dataset(mask_path='../dat/qd_imd/test/')
validation_generator = data.DataLoader(validation_set, **params)


opt = torch.optim.Adam(NET.parameters(), lr=1e-5)
NET.train()

writer = SummaryWriter()
GLOBAL_STEP = 0

for epoch in range(max_epochs):
    for batch in training_generator:
        opt.zero_grad()
        masked_img = batch["masked_image"]
        mask = batch["mask"]
        pred, mask_ = NET(masked_img, mask)
        actual_loss = loss.l1_loss(pred, batch["image"], device)

        if GLOBAL_STEP % 1000 == 0:
            print(actual_loss)
            grids = create_grids(masked_img, pred)
            write_to_tensorboard(writer, grids, actual_loss, GLOBAL_STEP)

        write_to_tensorboard(writer, None, actual_loss, GLOBAL_STEP)
        actual_loss.backward()
        opt.step()
        torch.cuda.empty_cache()
        GLOBAL_STEP += 1

    model_path = os.path.join(checkpoint_path, str(epoch))
    torch.save(NET.state_dict(), model_path)
