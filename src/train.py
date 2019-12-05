"""
Train the model
"""

from torch.utils import data
import torch
import matplotlib.pyplot as plt
from model import DeFINe
from loader import Dataset
import numpy as np

RAND = np.random.randint(0, 255, (1, 3, 1024, 1024)) / 255


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")

NET = DeFINe(device=device)
NET.to(device)


params = {'batch_size': 2,
          'shuffle': True,
          'num_workers': 4}

max_epochs = 1

training_set = Dataset()
training_generator = data.DataLoader(training_set, **params)

validation_set = Dataset(mask_path='../dat/qd_imd/test/')
validation_generator = data.DataLoader(validation_set, **params)

for epoch in range(max_epochs):

    for batch in training_generator:
        fig, axis = plt.subplots(4, 2)
        axis[0][0].imshow(batch["image"][0])
        axis[0][1].imshow(batch["image"][1])
        axis[1][0].imshow(batch["masked_image"][0])
        axis[1][1].imshow(batch["masked_image"][1])
        axis[2][0].imshow(batch["mask"][0])
        axis[2][1].imshow(batch["mask"][1])
        test = batch["image"]
        img = batch["image"].permute(0, 3, 1, 2)

        mask = batch["mask"].permute(0, 3, 1, 2)

        res_img, _ = NET(img, mask)
        res_img = res_img.cpu().detach().numpy()
        res_img = res_img.transpose(0, 2, 3, 1)
        axis[3][0].imshow(res_img[0])
        axis[3][1].imshow(res_img[0])

        plt.show()
        input()
