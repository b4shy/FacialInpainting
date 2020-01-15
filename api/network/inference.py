"""
Prediction Demo
"""

import argparse
from collections import OrderedDict
import time
import cv2
import matplotlib.pyplot as plt
import torch
from network.model import DeFINe
import sys
import numpy as np
import os

def inference(image, mask):


    #parser = argparse.ArgumentParser(description="Path to model")
    #parser.add_argument('--ckt', help="Path to checkpoint", default="./1")

    #args = parser.parse_args()
    ckt_path = os.path.abspath(".") + "/network/1" #args.ckt #TODO evtl von Request abhängig
    image = image / 255  # Normalize

    print(os.path.isfile(os.path.abspath(".") + "/network/1"))
    print(ckt_path)

    #mask[:, :, 0] = mask[:, :, 2]
    #mask[:, :, 1] = mask[:, :, 2]
    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    mask = mask/255
    mask = 1 - mask

    print(mask.shape)

    masked_image = image.copy()
    masked_image[mask == 0] = 1

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    net = DeFINe()
    net.to(device)
    net.eval()

    state_dict = torch.load(ckt_path, map_location=torch.device('cpu'))
    net.load_state_dict(state_dict)

    masked_image = masked_image.reshape(1, 512, 512, 3)
    masked_image = torch.tensor(masked_image).float().to(device)
    mask = torch.tensor(mask).float().to(device)
    mask = mask.reshape(1, 512, 512, 3)

    pred = net(masked_image, mask)
    pred = pred.float().cpu().detach().numpy()
    pred = pred.transpose(0, 2, 3, 1)
    pred = pred.clip(min=0)
    pred = np.floor(pred * 255)

    pred = np.squeeze(pred, axis=0)


    return pred
