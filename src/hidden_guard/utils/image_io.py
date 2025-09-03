from __future__ import annotations
from PIL import Image
import numpy as np

def save_png(arr: np.ndarray, path: str):
    Image.fromarray(arr).save(path)
