"""
Train the model
"""

from torch.utils import data
from torch.utils.data.sampler import SubsetRandomSampler
import torch
import loss
from model import DeFINe
from loader import Dataset


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")

NET = DeFINe(device=device)
NET.to(device)


params = {'batch_size': 4,
          'shuffle': False,
          'num_workers': 1}

max_epochs = 4000

training_set = Dataset()
training_generator = data.DataLoader(training_set, **params, sampler=SubsetRandomSampler([0]))

validation_set = Dataset(mask_path='../dat/qd_imd/test/')
validation_generator = data.DataLoader(validation_set, **params)


opt = torch.optim.Adam(NET.parameters(), lr=0.0002)
NET.train()

for epoch in range(max_epochs):
    for batch in training_generator:
        opt.zero_grad()
        masked_img = batch["masked_image"]
        mask = batch["mask"]
        pred, mask_ = NET(masked_img, mask)
        actual_loss = loss.l_hole(pred, batch["image"], mask, device)
        if epoch % 100 == 0:
            print(epoch)
            print(actual_loss)
            model_path = f'../ckt/{epoch}'
            torch.save(NET.state_dict(), model_path)
        actual_loss.backward()
        opt.step()
        torch.cuda.empty_cache()
