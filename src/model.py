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
        self.encode = [
            PartialConv2d(3, 64, kernel_size=7, stride=2, multi_channel=True, return_mask=True),
            PartialConv2d(64, 128, kernel_size=5, stride=2, multi_channel=True, return_mask=True),

            PartialConv2d(128, 256, kernel_size=5, stride=2, multi_channel=True, return_mask=True),
            PartialConv2d(256, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True, return_mask=True),

            PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(512, 512, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(512, 256, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(256, 128, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(128, 64, kernel_size=3, stride=1, multi_channel=True, return_mask=True),
            PartialConv2d(64, 3, kernel_size=3, stride=1, multi_channel=True, return_mask=True)
        ]

    def forward(self, img):
        """
        Inference on image
        :param img: batch of numpy arrays [b, 3, h, w]
        :return: tensor with inpainted image [b, 3, h, w]
        """
        img = torch.tensor(img, dtype=torch.float)
        out1, mask1 = self.forward_block(self.encode[0], img, False)
        out2, mask2 = self.forward_block(self.encode[1], out1, True)

        return out1

    def forward_block(self, operation, tensor, use_batchnorm=True):
        """
        Runs ReLU and BatchNorm on Conv Output
        :param operation: Convolution Operation
        :param tensor: Image Output from last block
        :param use_batchnorm: Use BatchNorm?
        :return:
        """

        out, mask = operation(tensor)
        if use_batchnorm:
            out = nn.BatchNorm2d(operation.out_channels)(out)
        return nn.ReLU()(out), mask
