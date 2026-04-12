import cv2
import numpy as np

def apply_bokeh(img, ksize=15):
    return cv2.GaussianBlur(img, (ksize, ksize), 0)

def apply_vignette(img, strength=0.002):
    h, w = img.shape[:2]
    y, x = np.indices((h, w))
    cy, cx = h // 2, w // 2
    d = np.sqrt((x - cx)**2 + (y - cy)**2)
    mask = np.exp(-strength * d**2)
    return (img * mask[..., None]).astype(np.uint8)