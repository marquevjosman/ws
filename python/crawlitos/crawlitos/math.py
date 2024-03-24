import numpy as np


def normalizeVector(v: np.ndarray):
    return v / np.linalg.norm(v)
