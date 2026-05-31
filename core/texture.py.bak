import cv2
import numpy as np

def lbp_texture(gray):
    lbp = np.zeros_like(gray)
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            if dy == 0 and dx == 0:
                continue
            shifted = np.roll(gray, (dy,dx), axis=(0,1))
            lbp += (shifted > gray).astype(np.uint8)
    return lbp