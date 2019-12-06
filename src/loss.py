import torch


def l1_loss(prediction, orig_image, device):
    img = orig_image.permute(0, 3, 1, 2).float().to(device)
    return torch.nn.L1Loss()(prediction, img)