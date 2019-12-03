"""
This module implements models for Facial Inpainting
"""

import torch
import torch.nn as nn
from partialconv2d import PartialConv2d

class DeFINe(nn.Module):
    """
    This class implements the Deep Facial Inpainting Model
    """

    def __init__(self):
        super().__init__()

        # Now we define the model
        # The model is a Unet, but uses the partial convolutions from nvidia
        self.pconv1 = PartialConv2d(3, 64, kernel_size=7, stride=2, multi_channel=True, return_mask=True)
        self.pconv2 = PartialConv2d(64, 128, kernel_size=5, stride=2, multi_channel=True, return_mask=True)

        self.pconv3 = PartialConv2d(128, 256, kernel_size=5, stride=2, multi_channel=True, return_mask=True)
        self.pconv4 = PartialConv2d(256, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True)
        self.pconv5 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True)
        self.pconv6 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True)
        self.pconv7 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True)
        self.pconv8 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True)

        self.pconv9 = PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv10 = PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv11 = PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv12 = PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv13 = PartialConv2d(512, 256, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv14 = PartialConv2d(256, 128, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv15 = PartialConv2d(128, 64, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        self.pconv16 = PartialConv2d(64, 3, kernel_size=3, stride=1, multi_channel=True, return_mask=True)

    def forward(self, img):
        img = torch.tensor(img, dtype=torch.float)
        out1, mask1 = self.forward_block(self.pconv1, img, False)
        out2, mask2 = self.forward_block(self.pconv2, out1, True)

        return out1

    def forward_block(self, operation, tensor, bn=True):
        out, mask = operation(tensor)
        if bn:
            out = nn.BatchNorm2d(operation.out_channels)(out)
        return nn.ReLU()(out), mask
