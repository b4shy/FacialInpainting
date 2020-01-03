"""
Train the model
"""
import argparse
import os
from torch.utils import data
from torch.utils.tensorboard import SummaryWriter
import torch
from utils import create_grid, write_to_tensorboard
from loss import Loss
from model import DeFINe, Vgg16
from loader import Dataset

parser = argparse.ArgumentParser(description="Path to face images and masks")
parser.add_argument('--img_path', help='path to image folder (up to images512x512)',
                    default='/home/marci/mockdata/Faces/ffhq-dataset/images512x512')
parser.add_argument('--mask_path', help='path to image folder (up to train or test)',
                    default='/home/marci/mockdata/qd_imd/train')
parser.add_argument('--checkpoint_path', help='path to store the checkpoints',
                    default='../dat/qd_imd/train/')
parser.add_argument('--batch_size', help='batch Size', type=int,
                    default=2)
parser.add_argument('--learning_rate', help='Learning Rate', type=float,
                    default=5e-5)
parser.add_argument('--train_from_checkpoint', help='Path to checkpoint',
                    default=None)
parser.add_argument('--logdir', help='Path to Tensorboard Logs',
                    default="~/runs/default")


args = parser.parse_args()
faces_path = args.img_path
mask_path = args.mask_path
checkpoint_path = args.checkpoint_path
batch_size = args.batch_size
learning_rate = args.learning_rate
train_from_checkpoint = args.train_from_checkpoint
logdir = args.logdir

use_cuda = torch.cuda.is_available()
cuda_device_count = torch.cuda.device_count()
print(f'Cuda Devices: {cuda_device_count}')
device = torch.device("cuda:0" if use_cuda else "cpu")

NET = DeFINe()
vgg16_partial = Vgg16()


if cuda_device_count > 1:
    print("Use", cuda_device_count, "GPUs!")
    NET = torch.nn.DataParallel(NET)
    vgg16_partial = torch.nn.DataParallel(vgg16_partial)

if train_from_checkpoint:
    NET.load_state_dict(torch.load(train_from_checkpoint))


NET.to(device)
vgg16_partial.to(device)


params = {'batch_size': batch_size,
          'shuffle': True,
          'num_workers': 4}  # 0 for GPU debugging

max_epochs = 200

training_set = Dataset(faces_path=faces_path, mask_path=mask_path)
training_generator = data.DataLoader(training_set, **params)

# validation_set = Dataset(mask_path='../dat/qd_imd/test/')
# validation_generator = data.DataLoader(validation_set, **params)


opt = torch.optim.Adam(NET.parameters(), lr=learning_rate)
NET.train()
loss = Loss(vgg16_partial)

writer = SummaryWriter(logdir)
GLOBAL_STEP = 0


for epoch in range(max_epochs):
    for batch in training_generator:
        opt.zero_grad()
        masked_img = batch["masked_image"].to(device).float()
        mask = batch["mask"].to(device).float()
        image = batch["image"].to(device)
        pred = NET(masked_img, mask)

        loss.prepare_loss_calculation(pred, image, mask)
        loss_hole = loss.calculate_loss_hole()
        loss_valid = loss.calculate_loss_valid()
        perceptual_loss = loss.calculate_perceptual_loss()
        style_loss_out = loss.calculate_style_out_loss()
        style_loss_comp = loss.calculate_style_comp_loss()
        tv_loss = loss.calculate_tv_loss()
        actual_loss = loss_valid + 6*loss_hole + 0.05*perceptual_loss + \
                      120*(style_loss_out + style_loss_comp) + 0.1*tv_loss

        if GLOBAL_STEP % 3000 == 0:
            print(actual_loss)
            grid = create_grid(masked_img, pred)
            write_to_tensorboard(writer, grid, actual_loss, GLOBAL_STEP)

        write_to_tensorboard(writer, None, actual_loss, GLOBAL_STEP)
        actual_loss.backward()
        opt.step()
        torch.cuda.empty_cache()
        GLOBAL_STEP += 1

    model_path = os.path.join(checkpoint_path, str(epoch))
    torch.save(NET.state_dict(), model_path)
