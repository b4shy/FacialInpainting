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
    pp_gt = (1 - mask_permuted) * img_permuted
    pp_pred = (1 - mask_permuted) * prediction
    return torch.nn.L1Loss()(pp_gt, pp_pred)


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
    pp_gt = mask_permuted * img_permuted
    pp_pred = mask_permuted * prediction
    return torch.nn.L1Loss()(pp_gt, pp_pred)


def l_perceptual(vgg16_model, prediction, image, mask, device):
    image_permuted = image.permute(0, 3, 1, 2).float().to(device)
    mask_permuted = mask.permute(0, 3, 1, 2).to(device)
    pred = prediction.to(device)
    vgg16_gt_out = vgg16_model(image_permuted)
    torch.cuda.empty_cache()

    vgg16_pred_out = vgg16_model(pred)
    torch.cuda.empty_cache()

    comp = mask_permuted * image_permuted + (1-mask_permuted)*pred
    torch.cuda.empty_cache()

    vgg16_comp_out = vgg16_model(comp)
    torch.cuda.empty_cache()

    loss = 0
    for pred, gt, cmp in zip(vgg16_pred_out, vgg16_gt_out, vgg16_comp_out):
        loss += (torch.nn.L1Loss()(pred, gt) + torch.nn.L1Loss()(cmp, gt))

    return loss
