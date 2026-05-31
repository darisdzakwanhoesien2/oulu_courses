import cv2
import numpy as np


def lbp_texture(gray: np.ndarray) -> np.ndarray:
    """Compute a simple 8-neighbor Local Binary Pattern (LBP)-like map.

    Notes
    -----
    This implementation sums 8 binary comparisons (shifted > center), producing
    values in [0, 8]. It is a lightweight texture descriptor for visualization.
    """
    if gray.ndim != 2:
        raise ValueError("lbp_texture expects a 2D grayscale image")

    lbp = np.zeros_like(gray, dtype=np.uint8)

    # Compare each neighbor to the center pixel.
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            shifted = np.roll(gray, (dy, dx), axis=(0, 1))
            lbp += (shifted > gray).astype(np.uint8)

    return lbp

