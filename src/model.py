"""
This module implements models for Facial Inpainting
"""

import torch
import torch.nn as nn
from partialconv2d import PartialConv2d
import matplotlib.pyplot as plt

class DeFINe(nn.Module):
    """
    This class implements the Deep Facial Inpainting Model
    """

    def __init__(self, device):
        super().__init__()

        # Now we define the model
        # The model is a Unet, but uses the partial convolutions from nvidia
        self.device = device


        self.encode0 = PartialConv2d(3, 64, kernel_size=7, stride=2, multi_channel=True,
                                     return_mask=True, padding=3)
        self.encode1 = PartialConv2d(64, 128, kernel_size=5, stride=2, multi_channel=True,
                                     return_mask=True, padding=2)
        self.encode2 = PartialConv2d(128, 256, kernel_size=5, stride=2, multi_channel=True,
                                     return_mask=True, padding=2)
        self.encode3 = PartialConv2d(256, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        self.encode4 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        self.encode5 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        self.encode6 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        self.encode7 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)

        self.decode0 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode1 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode2 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode3 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode4 = PartialConv2d(768, 256, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode5 = PartialConv2d(384, 128, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode6 = PartialConv2d(192, 64, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        self.decode7 = PartialConv2d(67, 3, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)

    def forward(self, img, mask):
        """
        Inference on image
        :param img: batch of tensors [b, 3, h, w]
        :param mask: batch of masks [b, 3, h, w]
        :return: tensor with inpainted image [b, 3, h, w]
        """

        img = torch.tensor(img, dtype=torch.float, requires_grad=False).to(self.device)
        img = img.permute(0, 3, 1, 2)
        mask = torch.tensor(mask, dtype=torch.float, requires_grad=False).to(self.device)
        mask = mask.permute(0, 3, 1, 2)

        out0, mask0 = self.forward_encode_block(self.encode0, img, mask, False)
        out1, mask1 = self.forward_encode_block(self.encode1, out0, mask0, False)
        out2, mask2 = self.forward_encode_block(self.encode2, out1, mask1, False)
        out3, mask3 = self.forward_encode_block(self.encode3, out2, mask2, False)
        out4, mask4 = self.forward_encode_block(self.encode4, out3, mask3, False)
        out5, mask5 = self.forward_encode_block(self.encode5, out4, mask4, False)
        out6, mask6 = self.forward_encode_block(self.encode6, out5, mask5, False)
        out7, mask7 = self.forward_encode_block(self.encode7, out6, mask6, False)

        decode_out0, decode_mask0 = self.forward_decode_block(self.decode0, out7, mask7, out6, mask6)
        decode_out1, decode_mask1 = self.forward_decode_block(self.decode1, decode_out0, decode_mask0, out5, mask5)
        decode_out2, decode_mask2 = self.forward_decode_block(self.decode2, decode_out1, decode_mask1, out4, mask4)
        decode_out3, decode_mask3 = self.forward_decode_block(self.decode3, decode_out2, decode_mask2, out3, mask3)
        decode_out4, decode_mask4 = self.forward_decode_block(self.decode4, decode_out3, decode_mask3, out2, mask2)
        decode_out5, decode_mask5 = self.forward_decode_block(self.decode5, decode_out4, decode_mask4, out1, mask1)
        decode_out6, decode_mask6 = self.forward_decode_block(self.decode6, decode_out5, decode_mask5, out0, mask0)
        img_out, mask_out = self.forward_decode_block(self.decode7, decode_out6, decode_mask6, img, mask)

        return img_out, mask_out

    def forward_encode_block(self, operation, img_tensor, mask_tensor, use_batchnorm=False):
        """
        Runs one operation from the encode block
        Runs ReLU and (maybe)BatchNorm on Conv Output
        :param operation: Convolution Operation
        :param img_tensor: Image Output from last block
        :param mask_tensor: Mask Output from last block
        :param use_batchnorm: Use BatchNorm?
        :return:
        """

        out, mask = operation(img_tensor, mask_tensor)
        if use_batchnorm:
            out = nn.BatchNorm2d(operation.out_channels)(out)
        return nn.ReLU()(out), mask

    def forward_decode_block(self, operation, img_tensor, mask_tensor, concat_with_img, concat_with_mask,
                             use_batchnorm=False):
        """
        Runs one operation from the decode block
        First Upsamples with
        Runs LeakyReLU and (maybe)BatchNorm on Conv Output

        :param operation: Operation from the Decode block
        :param img_tensor: Image Output from last block
        :param mask_tensor: Mask Output from last block
        :param concat_with_img: Concatenate with what layer?
        :param concat_with_mask: Concatenate with what layer?
        :param use_batchnorm:
        :return:
        """
        upsampled_img_tensor = nn.Upsample(scale_factor=2, mode="nearest")(img_tensor)
        upsampled_mask_tensor = nn.Upsample(scale_factor=2, mode="nearest")(mask_tensor)

        concat_img_tensor = torch.cat((upsampled_img_tensor, concat_with_img), dim=1)
        concat_mask_tensor = torch.cat((upsampled_mask_tensor, concat_with_mask), dim=1)
        out, mask = operation(concat_img_tensor, concat_mask_tensor)
        if use_batchnorm:
            out = nn.BatchNorm2d(operation.out_channels)(out)
        return nn.LeakyReLU(0.2)(out), mask

