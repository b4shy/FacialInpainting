from context import loss  # noqa
from context import model
import torch

use_cuda = torch.cuda.is_available()
DEVICE = torch.device("cpu")
PREDICTION = torch.zeros((1, 3, 512, 512))
ORIG_IMAGE = torch.zeros((1, 512, 512, 3))
MASK = torch.torch.ones((1, 512, 512, 3))

vgg16_partial = model.Vgg16()
vgg16_partial.to(DEVICE)

loss_calulator1 = loss.Loss(vgg16_partial, 20)
loss_calulator1.prepare_loss_calculation(PREDICTION, ORIG_IMAGE, MASK)


def test_loss_valid():
    loss_value = loss_calulator1.calculate_loss_valid()
    assert loss_value.item() == 0


def test_loss_hole():
    loss_value = loss_calulator1.calculate_loss_hole()
    assert loss_value.item() == 0


def test_perceptual_loss():
    loss_value = loss_calulator1.calculate_perceptual_loss()
    assert loss_value.item() == 0


def test_style_out_loss():
    loss_value = loss_calulator1.calculate_style_out_loss()
    assert loss_value.item() == 0


def test_style_comp_loss():
    loss_value = loss_calulator1.calculate_style_comp_loss()
    assert loss_value.item() == 0


PREDICTION_WRONG = torch.ones((1, 3, 512, 512))
ORIG_IMAGE = torch.zeros((1, 512, 512, 3))
MASK = torch.torch.ones((1, 512, 512, 3))
MASK[0][0][0][0] = 0

loss_calulator2 = loss.Loss(vgg16_partial, 20)
loss_calulator2.prepare_loss_calculation(PREDICTION_WRONG, ORIG_IMAGE, MASK)


def test_loss_valid_error():
    loss_value = loss_calulator2.calculate_loss_valid()
    assert loss_value.item() > 0.99


def test_loss_hole_error():
    loss_value = loss_calulator2.calculate_loss_hole()
    assert loss_value.item() < 0.1


def test_perceptual_loss_error():
    loss_value = loss_calulator2.calculate_perceptual_loss()
    assert not(loss_value.item() == 0)


def test_style_out_loss_error():
    loss_value = loss_calulator2.calculate_style_out_loss()
    assert not(loss_value.item() == 0)


def test_style_comp_loss_error():
    loss_value = loss_calulator2.calculate_style_comp_loss()
    assert not(loss_value.item() == 0)

