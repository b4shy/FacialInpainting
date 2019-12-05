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
    assert sample["image"].shape == (1024, 1024, 3)


def test_get_item_mask():
    sample = dataset[0]
    assert sample["masked_image"].shape == (1024, 1024, 3)


def test_overlay_image1():
    rnd_img = np.random.randint(0, 256, (1024, 1024, 3))
    rnd_mask = np.zeros((512, 512, 3))

    assert dataset.overlay_mask(rnd_img, rnd_mask).sum() == 0


def test_overlay_image2():
    rnd_img = np.random.randint(0, 256, (1024, 1024, 3))
    rnd_mask = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)

    assert not(dataset.overlay_mask(rnd_img, rnd_mask).sum() == 0)

