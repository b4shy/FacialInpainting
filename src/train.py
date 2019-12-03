"""
Train the model
"""
import numpy as np
from model import DeFINe

RAND = np.random.randint(0, 255, (1, 3, 1024, 1024)) / 255
NET = DeFINe()
NET(RAND)
