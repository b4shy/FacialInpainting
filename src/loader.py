"""
Data Loader Class
"""
import os
import random
from torch.utils import data
import cv2
# https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel


class Dataset(data.Dataset):
    """
    Manages Data Loading
    """
    def __init__(self, faces_path='../dat/Faces/ffhq-dataset/images1024x1024/', mask_path='../dat/qd_imd/train/'):
        """
        Initialize Dataset
        :param faces_path: path to faces
        :param mask_path: path to masks
        """
        actual_file_path = os.path.dirname(os.path.abspath(__file__))

        self.faces_path = os.path.join(actual_file_path, faces_path)

        self.mask_path = os.path.join(actual_file_path, mask_path)
        self.full_faces_path = []
        self.full_mask_path = []
        self.load_faces_paths()
        self.load_mask()

    def __len__(self):
        """

        :return: length of the dataset
        """
        return len(self.full_faces_path)

    def __getitem__(self, index):
        """
        Generates one sample of data
        The masks have the following form: 1024x1024x3. The value is 255 for No Drawing and 0 for the mask.
        We divide the mask by 255. The result is a matrix with 1 for No Inpainting and 0 for painting.
        Multiply this with the image and the corresponding pixel turn black
        :param item: Which item to return
        :return:
        """

        image_id = self.full_faces_path[index]
        image = cv2.imread(image_id)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        rnd_mask_index = random.randrange(0, len(self.full_mask_path))
        mask_id = self.full_mask_path[rnd_mask_index]
        mask = cv2.imread(mask_id)
        masked_image = self.overlay_mask(image, mask)

        sample = {"image": image, "masked_image": masked_image}
        return sample

    def overlay_mask(self, image, mask):
        """
        :param image: Image
        :param mask: Mask
        :return: Image fused with mask
        """
        mask = cv2.resize(mask, (1024, 1024))
        mask = mask / 255
        masked_image = (image * mask).astype(int)
        return masked_image

    def load_faces_paths(self):
        """
        Creates a list, containing the relative paths to the face images
        :return:
        """
        for i in os.listdir(self.faces_path):

            try:
                face_images = os.listdir(os.path.join(self.faces_path, i))
            except NotADirectoryError:
                continue
            for face in face_images:
                path_to_face = os.path.join(self.faces_path, i)
                self.full_faces_path.append(os.path.join(path_to_face, face))

    def load_mask(self):
        """
        Creates a list, containing the relative paths to the masks
        :return:
        """
        for i in os.listdir(self.mask_path):
            self.full_mask_path.append(os.path.join(self.mask_path, i))
