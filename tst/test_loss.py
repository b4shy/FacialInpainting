from context import loss  # noqa
import torch

use_cuda = torch.cuda.is_available()
DEVICE = torch.device("cuda:0" if use_cuda else "cpu")


def test_l1_loss_zeros():
    prediction = torch.zeros((1, 3, 512, 512))
    orig_image = torch.zeros((1, 512, 512, 3))
    device = DEVICE
    loss_value = loss.l1_loss(prediction, orig_image, device)
    assert loss_value.item() == 0


def test_l1_loss_error():
    prediction = torch.zeros((1, 3, 512, 512))
    orig_image = torch.ones((1, 512, 512, 3))
    device = DEVICE
    loss_value = loss.l1_loss(prediction, orig_image, device)
    assert loss_value.item() == 1



