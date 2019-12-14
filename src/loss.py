"""
Implement all the losses needed for the Inpainting.
"""
import torch


def l1_loss(prediction, orig_image, device):
    """
    Calculates normal l1 loss
    :param prediction: Predicted image
    :param orig_image: Originial image
    :param device: device CPU or CUDA
    :return: l1 loss
    """
    img = orig_image.permute(0, 3, 1, 2).float().to(device)
    return torch.nn.L1Loss()(prediction, img)


def l_hole(prediction, orig_image, mask, device):
    """
    L hole loss according to the paper
    @param prediction: Predicted Image
    @param orig_image: Label
    @param mask: Mask which was used to overlay the image
    @param device: Device: CPU or CUDA
    """
    img_permuted = orig_image.permute(0, 3, 1, 2).float().to(device)
    mask_permuted = mask.permute(0, 3, 1, 2).float().to(device)
    res = torch.mean(torch.abs((1 - mask_permuted) * (prediction - img_permuted)))
    return res


def l_valid(prediction, orig_image, mask, device):
    """
    L valid loss according to the paper
    @param prediction: Predicted Image
    @param orig_image: Label
    @param mask: Mask which was used to overlay the image
    @param device: Device: CPU or CUDA
    """
    img_permuted = orig_image.permute(0, 3, 1, 2).float().to(device)
    mask_permuted = mask.permute(0, 3, 1, 2).float().to(device)
    res = torch.mean(torch.abs(mask_permuted * (prediction - img_permuted)))
    return res
