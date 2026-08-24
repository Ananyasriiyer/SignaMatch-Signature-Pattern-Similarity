from PIL import Image
import numpy as np

from config import (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    THRESHOLD
)


def load_image(image_path):
    """
    Open the signature image.
    """
    image = Image.open(image_path)

    return image


def convert_to_grayscale(image):
    """
    Convert the image into grayscale.
    """
    grayscale = image.convert("L")

    return grayscale


def resize_image(image):
    """
    Resize the image to 64 x 64 pixels.
    """
    resized = image.resize(
        (IMAGE_WIDTH, IMAGE_HEIGHT)
    )

    return resized


def convert_to_binary(image):
    """
    Convert the grayscale image
    into a binary NumPy matrix.
    """
    matrix = np.array(image)

    binary = matrix < THRESHOLD

    return binary


def preprocess_signature(image_path):
    """
    Complete signature image processing pipeline.
    """

    original = load_image(image_path)

    grayscale = convert_to_grayscale(
        original
    )

    resized = resize_image(
        grayscale
    )

    binary = convert_to_binary(
        resized
    )

    return {
        "original": original,
        "grayscale": grayscale,
        "resized": resized,
        "binary": binary
    }