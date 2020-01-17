"""
Prediction Demo
"""

import time
import logging
import numpy as np
import torch
from .model import DeFINe

class InferenceManager():
    logger = logging.getLogger(__name__)

    def __init__(self, neural_net: DeFINe, architecture: torch.device):
        self._neural_net = neural_net
        self._architecture = architecture
    
    def infer(self, image, mask):
        image = image / 255  # Normalize
        mask = self._prepare_mask(mask)
        masked_image = self._get_masked_image(image.copy(), mask)
        prediction = self._predict(masked_image, mask)

        return prediction
    
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
        mask = torch.tensor(mask).float().to(self._architecture)
        mask = mask.reshape(1, 512, 512, 3)
        self.logger.debug(mask.shape)
        return mask
    
    def _get_masked_image(self, image_copy, mask):
        masked_image = image_copy
        masked_image[mask == 0] = 1

        masked_image = masked_image.reshape(1, 512, 512, 3)
        masked_image = torch.tensor(masked_image).float().to(self._architecture)
        return masked_image
        

def inference(net, image, mask, device):
    logger = logging.getLogger(__name__)
    image = image / 255  # Normalize
    mask[mask > 0] = 255

    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    mask = mask/255
    mask = 1 - mask

    logger.info(mask.shape)

    masked_image = image.copy()
    masked_image[mask == 0] = 1


    masked_image = masked_image.reshape(1, 512, 512, 3)
    masked_image = torch.tensor(masked_image).float().to(device)
    mask = torch.tensor(mask).float().to(device)
    mask = mask.reshape(1, 512, 512, 3)
    tic = time.time()
    pred = net(masked_image, mask)
    logger.info(time.time() - tic)
    pred = pred.float().cpu().detach().numpy()
    pred = pred.transpose(0, 2, 3, 1)
    pred = np.floor(pred * 255)

    pred = np.squeeze(pred, axis=0)


    return pred
