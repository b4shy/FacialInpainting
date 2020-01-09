from context import utils
import torch

masked_image = torch.zeros((1, 512, 512, 3))
prediction = torch.zeros((1, 3, 512, 512))


def test_create_grid():
    grid = utils.create_grid(masked_image, prediction)
    assert grid.shape == torch.Size([3, 1024, 512])

