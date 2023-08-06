import os
import random

import numpy as np


def seed_everything(seed: int) -> None:
    """
    Sets random seed globally.

    Arguments:
        seed: the seed to fix globally
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
