from context import loader  # noqa
import numpy as np
import os
path = os.path.abspath(os.path.dirname(__file__))

face_path = f'{path}/mock/Faces'
mask_path = f'{path}/mock/mask'
dataset = loader.Dataset(faces_path=face_path, mask_path=mask_path)


def test_init():
    assert len(dataset.full_mask_path) == 1


def test_init_2():
    assert len(dataset.full_faces_path) == 1


def test_length():
    assert len(dataset) == 1


def test_get_item_type():
    sample = dataset[0]
    assert isinstance(sample, dict)


def test_get_item_image():
    sample = dataset[0]
    assert sample["image"].shape == (512, 512, 3)


def test_get_item_mask():
    sample = dataset[0]
    assert sample["masked_image"].shape == (512, 512, 3)


def test_overlay_image1():
    rnd_img = np.random.randint(0, 256, (512, 512, 3))
    rnd_mask = np.zeros((512, 512, 3))
    masked_image = dataset.overlay_mask(rnd_img, rnd_mask)

    assert masked_image.sum() == 512*512*3


def test_imgs_are_normalized():
    assert (dataset[0]["image"].max() == 1)


def test_masks_are_normalized():
    assert (dataset[0]["mask"].min() == 0) and (dataset[0]["mask"].max() == 1)


def test_masked_images_are_normalized():
    assert (dataset[0]["masked_image"].max() == 1)
