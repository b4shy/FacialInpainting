"""
Utils for tensorboard etc
"""
import torchvision


def create_grids(masked_imgs, predicted_imgs):
    """
    masked_imgs: masked input image
    predicted_imgs: predicted images from the Network
    """
    masked_img_permute = masked_imgs.permute(0, 3, 1, 2)
    grid_masked_image = torchvision.utils.make_grid(masked_img_permute)
    grid_predicted_image = torchvision.utils.make_grid(predicted_imgs)
    return grid_masked_image, grid_predicted_image


def write_to_tensorboard(writer, grids, actual_loss,  GLOBAL_STEP):
    masked_grid, predicted_grid = grids
    writer.add_image("images", masked_grid, global_step=GLOBAL_STEP)
    writer.add_image("Predictions", predicted_grid, global_step=GLOBAL_STEP)
    writer.add_scalar('Loss', actual_loss, global_step=GLOBAL_STEP)
