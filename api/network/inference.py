"""
Prediction Demo
"""

import time
import logging
import numpy as np

import torch



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
