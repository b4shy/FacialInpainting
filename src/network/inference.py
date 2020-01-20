"""
Prediction Demo
"""

import logging
import numpy as np
import torch
from .model import DeFINe

class InferenceManager():
    logger = logging.getLogger(__name__)

    def __init__(self, neural_net: DeFINe, architecture: torch.device):
        self._neural_net = neural_net
        self._architecture = architecture
        self.prediction = None
    
    def infer(self, image, mask):
        image = image / 255  # Normalize
        mask = self._prepare_mask(mask)
        masked_image = self._get_masked_image(image, mask)
        mask = self._reshape_mask(mask)
        self.prediction = self._predict(masked_image, mask)

        return self.prediction
    
    def _predict(self, masked_image, mask):
        self.logger.debug("Starting the prediction.")
        prediction = self._neural_net(masked_image, mask)
        self.logger.debug("Finished the prediction.")

        prediction = prediction.float().cpu().detach().numpy()
        prediction = prediction.transpose(0, 2, 3, 1)
        prediction = np.floor(prediction * 255)
        prediction = np.squeeze(prediction, axis=0)
        return prediction
    
    def _prepare_mask(self, mask):
        mask[mask > 0] = 255
        mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
        mask = mask / 255
        mask = 1 - mask
        self.logger.debug(mask.shape)
        return mask

    def _reshape_mask(self, mask):
        mask = torch.tensor(mask).float().to(self._architecture)
        mask = mask.reshape(1, 512, 512, 3)
        self.logger.debug(mask.shape)
        return mask
    
    def _get_masked_image(self, image, mask):
        masked_image = image.copy()
        masked_image[mask == 0] = 1

        masked_image = masked_image.reshape(1, 512, 512, 3)
        masked_image = torch.tensor(masked_image).float().to(self._architecture)
        return masked_image