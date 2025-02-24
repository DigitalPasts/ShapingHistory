import numpy as np
import cv2
from PIL import Image

def verify_image_input(image):
    """
    Verifies that the input is a valid image.
    Args: image (np.ndarray): Input image.
    Raises: ValueError: If the input is not a valid image.
    """
    if not isinstance(image, np.ndarray):
        raise ValueError("Input must be a numpy array.")
    if image.ndim not in [2, 3]:
        raise ValueError("Input image must have 2 or 3 dimensions.")
    if image.ndim == 3 and image.shape[2] not in [1, 3, 4]:
        raise ValueError("Input image must have 1, 3, or 4 channels.")
    if image.size == 0:
        raise ValueError("Input image cannot be empty.")
    if image.dtype not in [np.uint8, np.float32]:
        raise ValueError("Input image must be of type uint8 or float32.")

def resize_image(image, size=(500, 500)):
    """
    Resizes an image to fit within the specified size while maintaining the aspect ratio.
    Pads the image with black borders if necessary to match the exact size.
    Args: image (np.ndarray): Input image.
    size (tuple): Desired output size (height, width).
    Returns: np.ndarray: Resized and padded image.
    """
    verify_image_input(image)
    h, w = image.shape[:2]
    scale = min(size[0] / h, size[1] / w)
    new_h, new_w = int(h * scale), int(w * scale)
    resized_image = cv2.resize(image, (new_w, new_h))
    top = (size[0] - new_h) // 2
    bottom = size[0] - new_h - top
    left = (size[1] - new_w) // 2
    right = size[1] - new_w - left
    return cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

def to_greyscale(image):
    """
    Converts a BGR image to grayscale.
    Args: image (np.ndarray): Input BGR image.
    Returns: np.ndarray: Grayscale image.
    """
    verify_image_input(image)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def create_mask(image):
    """
    Enhances contrast, applies Gaussian blur, and thresholds the image to create a binary mask.
    Args: image (np.ndarray): Input grayscale image (uint8 or float32).
    Returns: np.ndarray: Binary mask (float32, values 0 or 1).
    """
    verify_image_input(image)
    
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = to_greyscale(image)
    
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)
    
    alpha = 3.0  
    beta = 0     
    enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    enhanced = enhanced.astype(np.float32) / 255.0
    blurred = cv2.GaussianBlur(enhanced, (11, 11), 0)

    _, mask = cv2.threshold(blurred, 0.125, 1.0, cv2.THRESH_BINARY)

    return (mask*255).astype(np.uint8)