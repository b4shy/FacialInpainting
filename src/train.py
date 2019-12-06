"""
Train the model
"""

from torch.utils import data
from torch.utils.data.sampler import SubsetRandomSampler
import torch
import loss
import matplotlib.pyplot as plt
from model import DeFINe
from loader import Dataset


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")

NET = DeFINe(device=device)
NET.to(device)


params = {'batch_size': 4,
          'shuffle': False,
          'num_workers': 4}

max_epochs = 300

training_set = Dataset()
training_generator = data.DataLoader(training_set, **params, sampler=SubsetRandomSampler([0]))

validation_set = Dataset(mask_path='../dat/qd_imd/test/')
validation_generator = data.DataLoader(validation_set, **params)


opt = torch.optim.Adam(NET.parameters(), lr=1e-4)
NET.train()

for epoch in range(max_epochs):
    for batch in training_generator:
        opt.zero_grad()
        masked_img = batch["masked_image"]
        mask = batch["masked_image"]
        pred, mask_ = NET(masked_img, mask)
        actual_loss = loss.l1_loss(pred, batch["image"], device)
        print(actual_loss)
        actual_loss.backward()
        opt.step()
        torch.cuda.empty_cache()

pred, mask = NET(batch["masked_image"], batch["mask"])

fig, axis = plt.subplots(1, 2)
axis[0].imshow(batch["masked_image"][0].reshape(512, 512, 3))
pred = pred.int().cpu().detach().numpy()
pred = pred.transpose(0, 2, 3, 1)
axis[1].imshow(pred[0])
plt.show()
