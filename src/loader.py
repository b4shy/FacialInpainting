"""
Data Loader Class
"""
from torch.utils import data
import torch
# https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel


class Dataset(data.Dataset):
    """
    Manages Data Loading
    """
    def __init__(self, list_ids):
        """
        Initialize Dataset
        :param list_ids: list containing the image ids
        """
        self.list_ids = list_ids

    def __len__(self):
        """

        :return: length of the dataset
        """
        return len(self.list_ids)

    def __getitem__(self, index):
        """
        Generates one sample of data
        :param item: Which item to return
        :return:
        """

        image_id = self.list_ids[index]
        path = f'../dat{image_id}.png'
        image = torch.load(path)
        mask = torch.load("mask_path")
        masked_image = self.overlay_mask(image, mask)

        return masked_image, image

    def overlay_mask(self, image, mask):
        """

        :param image: Image
        :param mask: Mask
        :return: Image fused with mask
        """
        masked_image = image + mask
        return masked_image
