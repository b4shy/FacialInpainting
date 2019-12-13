"""
Prediction Demo
"""

import time
import cv2
import matplotlib.pyplot as plt
import torch
from model import DeFINe

img0_path = f'../dat/1.png'
mask0_path = f'../dat/mask_00000_train.png'
image = cv2.imread(img0_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (512, 512))
image = image / 255  # Normalize

mask = cv2.imread(mask0_path)
masked_image = image.copy()
masked_image[mask == 0] = 1

use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
net = DeFINe()
net.to(device)
net.load_state_dict(torch.load("../ckt/0", map_location=torch.device('cpu')))
net.eval()

masked_image = masked_image.reshape(1, 512, 512, 3)
masked_image = torch.tensor(masked_image).float()
mask = torch.tensor(mask).float()
mask = mask.reshape(1, 512, 512, 3)
tic = time.time()
pred = net(masked_image, mask)
print(time.time() - tic)
pred = pred.float().cpu().detach().numpy()
pred = pred.transpose(0, 2, 3, 1)

fig, axis = plt.subplots(2, 2, figsize=(10, 10))

axis[0][0].imshow(mask[0])
axis[0][0].set_title("Mask")
axis[0][1].imshow(image)
axis[0][1].set_title("Image")
axis[1][0].imshow(masked_image[0])
axis[1][0].set_title("Image with Mask")
axis[1][1].imshow(pred[0])
axis[1][1].set_title("Prediction")

plt.axis('off')

plt.show()
