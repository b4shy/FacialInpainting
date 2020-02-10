"""
This module implements models for Facial Inpainting
"""
from collections import namedtuple
import torch
import torch.nn as nn
from partialconv2d import PartialConv2d
from torch.nn.init import kaiming_normal_
import torchvision


class DeFINe(nn.Module):
    """
    This class implements the Deep Facial Inpainting Model
    """

    def __init__(self, ):
        super().__init__()

        # Now we define the model
        # The model is a Unet, but uses the partial convolutions from nvidia

        self.encode0 = PartialConv2d(3, 64, kernel_size=7, stride=2, multi_channel=True,
                                     return_mask=True, padding=3)
        kaiming_normal_(self.encode0.weight, nonlinearity='relu')

        self.encode1 = PartialConv2d(64, 128, kernel_size=5, stride=2, multi_channel=True,
                                     return_mask=True, padding=2)
        kaiming_normal_(self.encode1.weight, nonlinearity='relu')
        self.batchnorm1 = nn.BatchNorm2d(128)

        self.encode2 = PartialConv2d(128, 256, kernel_size=5, stride=2, multi_channel=True,
                                     return_mask=True, padding=2)
        kaiming_normal_(self.encode2.weight, nonlinearity='relu')
        self.batchnorm2 = nn.BatchNorm2d(256)

        self.encode3 = PartialConv2d(256, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.encode3.weight, nonlinearity='relu')
        self.batchnorm3 = nn.BatchNorm2d(512)

        self.encode4 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.encode4.weight, nonlinearity='relu')
        self.batchnorm4 = nn.BatchNorm2d(512)

        self.encode5 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.encode5.weight, nonlinearity='relu')
        self.batchnorm5 = nn.BatchNorm2d(512)

        self.encode6 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.encode6.weight, nonlinearity='relu')
        self.batchnorm6 = nn.BatchNorm2d(512)

        self.encode7 = PartialConv2d(512, 512, kernel_size=3, stride=2, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.encode7.weight, nonlinearity='relu')
        self.batchnorm7 = nn.BatchNorm2d(512)

        # Decoding Layers
        self.decode0 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode0.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm8 = nn.BatchNorm2d(512)

        self.decode1 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode1.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm9 = nn.BatchNorm2d(512)

        self.decode2 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode2.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm10 = nn.BatchNorm2d(512)

        self.decode3 = PartialConv2d(1024, 512, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode3.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm11 = nn.BatchNorm2d(512)

        self.decode4 = PartialConv2d(768, 256, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode4.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm12 = nn.BatchNorm2d(256)

        self.decode5 = PartialConv2d(384, 128, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode5.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm13 = nn.BatchNorm2d(128)

        self.decode6 = PartialConv2d(192, 64, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode6.weight, a=0.2, nonlinearity='leaky_relu')
        self.batchnorm14 = nn.BatchNorm2d(64)

        self.decode7 = PartialConv2d(67, 3, kernel_size=3, stride=1, multi_channel=True,
                                     return_mask=True, padding=1)
        kaiming_normal_(self.decode7.weight, a=0.2, nonlinearity='leaky_relu')

    def forward(self, masked_image, input_mask):
        """
        Inference on image
        :param masked_image: batch of tensors [b, 3, h, w]
        :param input_mask: batch of masks [b, 3, h, w]
        :return: tensor with inpainted image [b, 3, h, w]
        """
        img = masked_image.permute(0, 3, 1, 2)
        mask = input_mask.permute(0, 3, 1, 2)

        out0, mask0 = self.forward_encode_block(self.encode0, img, mask, None)
        out1, mask1 = self.forward_encode_block(self.encode1, out0, mask0, self.batchnorm1)
        out2, mask2 = self.forward_encode_block(self.encode2, out1, mask1, self.batchnorm2)
        out3, mask3 = self.forward_encode_block(self.encode3, out2, mask2, self.batchnorm3)
        out4, mask4 = self.forward_encode_block(self.encode4, out3, mask3, self.batchnorm4)
        out5, mask5 = self.forward_encode_block(self.encode5, out4, mask4, self.batchnorm5)
        out6, mask6 = self.forward_encode_block(self.encode6, out5, mask5, self.batchnorm6)
        out7, mask7 = self.forward_encode_block(self.encode7, out6, mask6, self.batchnorm7)

        decode_out0, decode_mask0 = self.forward_decode_block(self.decode0, out7, mask7,
                                                              out6, mask6, self.batchnorm8)
        decode_out1, decode_mask1 = self.forward_decode_block(self.decode1, decode_out0, decode_mask0,
                                                              out5, mask5, self.batchnorm9)
        decode_out2, decode_mask2 = self.forward_decode_block(self.decode2, decode_out1, decode_mask1,
                                                              out4, mask4, self.batchnorm10)
        decode_out3, decode_mask3 = self.forward_decode_block(self.decode3, decode_out2, decode_mask2,
                                                              out3, mask3, self.batchnorm11)
        decode_out4, decode_mask4 = self.forward_decode_block(self.decode4, decode_out3, decode_mask3,
                                                              out2, mask2, self.batchnorm12)
        decode_out5, decode_mask5 = self.forward_decode_block(self.decode5, decode_out4, decode_mask4,
                                                              out1, mask1, self.batchnorm13)
        decode_out6, decode_mask6 = self.forward_decode_block(self.decode6, decode_out5, decode_mask5,
                                                              out0, mask0, self.batchnorm14)
        img_out, mask_out = self.forward_decode_block(self.decode7, decode_out6, decode_mask6, img, mask, None)

        return img_out

    @staticmethod
    def forward_encode_block(operation, img_tensor, mask_tensor, batch_norm_op):
        """
        Runs one operation from the encode block
        Runs ReLU and (maybe)BatchNorm on Conv Output
        :param operation: Convolution Operation
        :param img_tensor: Image Output from last block
        :param mask_tensor: Mask Output from last block
        :param batch_norm_op: Use above defined batchnorm. None if no batchnorm shall be applied
        :return: Operation Result
        """

        out, mask = operation(img_tensor, mask_tensor)
        if batch_norm_op:
            out = batch_norm_op(out)
        return nn.ReLU()(out), mask

    @staticmethod
    def forward_decode_block( operation, img_tensor, mask_tensor, concat_with_img, concat_with_mask, batch_norm_op):
        """
        Runs one operation from the decode block
        First Upsamples with
        Runs LeakyReLU and (maybe)BatchNorm on Conv Output

        :param operation: Operation from the Decode block
        :param img_tensor: Image Output from last block
        :param mask_tensor: Mask Output from last block
        :param concat_with_img: Concatenate with what layer?
        :param concat_with_mask: Concatenate with what layer?
        :param batch_norm_op: Use above defined batchnorm. None if no batchnorm shall be applied
        :return: Operation Result
        """
        upsampled_img_tensor = nn.Upsample(scale_factor=2, mode="nearest")(img_tensor)
        upsampled_mask_tensor = nn.Upsample(scale_factor=2, mode="nearest")(mask_tensor)

        concat_img_tensor = torch.cat((upsampled_img_tensor, concat_with_img), dim=1)
        concat_mask_tensor = torch.cat((upsampled_mask_tensor, concat_with_mask), dim=1)
        out, mask = operation(concat_img_tensor, concat_mask_tensor)
        if batch_norm_op:
            out = batch_norm_op(out)
        return nn.LeakyReLU(0.2)(out), mask


class Vgg16(torch.nn.Module):
    """
    Partial VGG16 Model.
    Code expanded with Normalization and adapted Output from the pytorch example:
    https://github.com/pytorch/examples/blob/master/fast_neural_style/neural_style/vgg.py
    Returns the 3 Max Pool Layers
    """
    def __init__(self):
        """
        Creates the three slices to return the Max-Pool Outputs
        """
        super(Vgg16, self).__init__()
        vgg_pretrained_features = torchvision.models.vgg16(pretrained=True).features
        self.slice1 = torch.nn.Sequential()
        self.slice2 = torch.nn.Sequential()
        self.slice3 = torch.nn.Sequential()
        for x in range(5):
            self.slice1.add_module(str(x), vgg_pretrained_features[x])
        for x in range(5, 10):
            self.slice2.add_module(str(x), vgg_pretrained_features[x])
        for x in range(10, 17):
            self.slice3.add_module(str(x), vgg_pretrained_features[x])
        for param in self.parameters():
            param.requires_grad = False

    def forward(self, x):
        """
        Returns the three MaxPool Outputs
        :param x: Input Batch
        :returns: Namedtuple containing the three Maxpool outputs
        """
        x = self.normalize(x)
        h = self.slice1(x)
        h_maxpool_1 = h
        h = self.slice2(h)
        h_maxpool_2 = h
        h = self.slice3(h)
        h_maxpool_3 = h
        vgg_outputs = namedtuple("VggOutputs", ['maxpool_1', 'maxpool_2', 'maxpool_3'])
        out = vgg_outputs(h_maxpool_1, h_maxpool_2, h_maxpool_3)
        return out

    @staticmethod
    def normalize(x):
        """
        Normalize according to image Net (VGG is trained on it)
        :param x: Input batch
        :returns: The normalized Input Batch according to ImageNet
        """
        mean = x.data.new(x.data.size())
        std = x.data.new(x.data.size())
        mean[:, 0, :, :] = 0.485
        mean[:, 1, :, :] = 0.456
        mean[:, 2, :, :] = 0.406
        std[:, 0, :, :] = 0.229
        std[:, 1, :, :] = 0.224
        std[:, 2, :, :] = 0.225
        x_norm = x - mean
        x_norm = x_norm / std
        return x_norm

