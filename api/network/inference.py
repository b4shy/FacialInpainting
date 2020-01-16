"""
Prediction Demo
"""

import argparse
from collections import OrderedDict
import time
import cv2
import matplotlib.pyplot as plt
import torch
import sys
import numpy as np
import os

def inference(net, image, mask, device):


    #parser = argparse.ArgumentParser(description="Path to model")
    #parser.add_argument('--ckt', help="Path to checkpoint", default="./1")

    #args = parser.parse_args()
    image = image / 255  # Normalize
    mask[mask > 0] = 255

    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    mask = mask/255
    mask = 1 - mask

    print(mask.shape)

    masked_image = image.copy()
    masked_image[mask == 0] = 1


    masked_image = masked_image.reshape(1, 512, 512, 3)
    masked_image = torch.tensor(masked_image).float().to(device)
    mask = torch.tensor(mask).float().to(device)
    mask = mask.reshape(1, 512, 512, 3)
    tic = time.time()
    pred = net(masked_image, mask)
    print(time.time() - tic)
    pred = pred.float().cpu().detach().numpy()
    pred = pred.transpose(0, 2, 3, 1)
    pred = np.floor(pred * 255)

    pred = np.squeeze(pred, axis=0)


    return pred
