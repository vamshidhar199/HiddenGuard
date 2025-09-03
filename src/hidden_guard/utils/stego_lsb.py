from __future__ import annotations
from PIL import Image
import numpy as np
import random

def _msg_bits(msg: str):
    for ch in msg.encode("utf-8"):
        for i in range(8):
            yield (ch >> i) & 1

def embed_lsb(image_path: str, out_path: str, message: str, channel: int = 2):
    """
    Embed message bits into the least significant bit of the specified channel (0=R/1=G/2=B).
    """
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img).copy()
    h, w, _ = arr.shape
    npx = h * w
    bits = list(_msg_bits(message))
    if len(bits) > npx:
        raise ValueError("Message too long for image size")

    # Choose pseudo-random positions but deterministic (seed on message length for demo)
    random.seed(len(message))
    positions = random.sample(range(npx), len(bits))

    for bit, pos in zip(bits, positions):
        y, x = divmod(pos, w)
        arr[y, x, channel] = (arr[y, x, channel] & ~1) | (bit & 1)

    Image.fromarray(arr).save(out_path)

def make_noise_image(path: str, size=(256,256), seed: int = 0):
    rng = np.random.default_rng(seed)
    arr = (rng.integers(0, 255, size=(size[1], size[0], 3))).astype(np.uint8)
    Image.fromarray(arr).save(path)
