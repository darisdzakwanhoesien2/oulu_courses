import numpy as np


def white_balance(img: np.ndarray) -> np.ndarray:
    """Apply simple gray-world white balance.

    Parameters
    ----------
    img:
        RGB image as a NumPy array with shape (H, W, 3) and values in [0, 255].

    Returns
    -------
    np.ndarray
        White-balanced RGB image (uint8).
    """
    img_f32 = img.astype(np.float32)

    means = img_f32.mean(axis=(0, 1))
    gray = means.mean()

    # Avoid division by zero if a channel mean is 0.
    scale = gray / np.clip(means, 1e-6, None)
    img_f32 *= scale

    return np.clip(img_f32, 0, 255).astype(np.uint8)

