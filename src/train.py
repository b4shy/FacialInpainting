"""
Train the model
"""

from torch.utils import data
import torch
import matplotlib.pyplot as plt
from model import DeFINe
from loader import Dataset

#RAND = np.random.randint(0, 255, (1, 3, 1024, 1024)) / 255
#NET = DeFINe()
#NET(RAND)


use_cuda = torch.cuda.is_available()
print(use_cuda)
device = torch.device("cuda" if use_cuda else "cpu")
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
        print(batch["image"].shape)
        fig, axis = plt.subplots(2, 2)
        axis[0][0].imshow(batch["image"][0])
        axis[0][1].imshow(batch["image"][1])
        axis[1][0].imshow(batch["masked_image"][0])
        axis[1][1].imshow(batch["masked_image"][1])
        plt.show()
        input()
