"""
Utils for tensorboard etc
"""
import torchvision
import torch


def create_grid(masked_imgs, predicted_imgs):
    """
    masked_imgs: masked input image
    predicted_imgs: predicted images from the Network
    """
    masked_img_permute = masked_imgs.permute(0, 3, 1, 2)
    concatted_images = torch.cat((predicted_imgs, masked_img_permute), 2)
    grid = torchvision.utils.make_grid(concatted_images)
    return grid


def write_to_tensorboard(writer, grid, actual_loss, GLOBAL_STEP):
    """
    :param writer: Tensorboard writer
    :param grid: Image Grid, None if only the loss shall be added
    :param actual_loss: actual loss
    :param GLOBAL_STEP: Actual Step
    :return: Nothing
    """

    if grid is not None:
        writer.add_image("Predictions and Inputs", grid, global_step=GLOBAL_STEP)
    writer.add_scalar('Loss', actual_loss, global_step=GLOBAL_STEP)
