"""
Implement all the losses needed for the Inpainting.
"""
import torch


def l1_loss(prediction, orig_image, device):
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

    pp_gt = (1 - mask_permuted) * img_permuted
    pp_pred = (1 - mask_permuted) * prediction
    return torch.nn.L1Loss()(pp_gt, pp_pred)
