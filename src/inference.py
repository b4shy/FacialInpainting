"""
Prediction Demo
"""

import argparse
from collections import OrderedDict
import time
import cv2
import matplotlib.pyplot as plt
import torch
from model import DeFINe
parser = argparse.ArgumentParser(description="Path to model")
parser.add_argument('--ckt', help="Path to checkpoint", default="../ckt/0")

args = parser.parse_args()
ckt_path = args.ckt

img0_path = f'../dat/4.png'
mask0_path = f'../dat/mask_00014_test.png'
image = cv2.imread(img0_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (512, 512))
image = image / 255  # Normalize

mask = cv2.imread(mask0_path)
mask = mask/255
mask = cv2.rotate(mask, cv2.ROTATE_90_CLOCKWISE)

masked_image = image.copy()
masked_image[mask == 0] = 1

use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
net = DeFINe()
net.to(device)
net.eval()

state_dict = torch.load(ckt_path, map_location=torch.device('cpu'))
net.load_state_dict(state_dict)
# new_state_dict = OrderedDict()
# for k, v in state_dict.items():
#    name = k[7:] # remove module.
#    new_state_dict[name] = v

# net.load_state_dict(new_state_dict)

masked_image = masked_image.reshape(1, 512, 512, 3)
masked_image = torch.tensor(masked_image).float().to(device)
mask = torch.tensor(mask).float().to(device)
mask = mask.reshape(1, 512, 512, 3)
tic = time.time()
pred = net(masked_image, mask)
print(time.time() - tic)
pred = pred.float().cpu().detach().numpy()
pred = pred.transpose(0, 2, 3, 1)

fig, axis = plt.subplots(2, 2, figsize=(10, 10))

axis[0][0].imshow(mask[0].cpu())
axis[0][0].set_title("Mask")
axis[0][0].axis("off")

axis[0][1].imshow(image)
axis[0][1].set_title("Image")
axis[0][1].axis("off")
axis[1][0].imshow(masked_image[0].cpu())
axis[1][0].set_title("Image with Mask")
axis[1][0].axis("off")
axis[1][1].imshow(pred[0])
axis[1][1].set_title("Prediction")
axis[1][1].axis("off")
plt.axis('off')

plt.show()
