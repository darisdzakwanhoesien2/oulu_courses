import numpy as np

def white_balance(img):
    img = img.astype(np.float32)
    means = img.mean(axis=(0,1))
    gray = means.mean()
    scale = gray / means
    img *= scale
    return np.clip(img, 0, 255).astype(np.uint8)