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
    Supports file paths, file-like objects (e.g. Streamlit UploadedFile),
    or already loaded PIL Image objects.
    """
    if isinstance(image_path, Image.Image):
        return image_path

    image = Image.open(image_path)

    return image


def convert_to_grayscale(image):
    """
    Convert the image into grayscale.
    Handles transparency by compositing onto a clean white canvas
    to avoid treating transparent backgrounds as black ink.
    """
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        rgba = image.convert("RGBA")
        white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        blended = Image.alpha_composite(white_bg, rgba)
        return blended.convert("L")

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


def convert_to_binary(image, threshold=None):
    """
    Convert the grayscale image into a binary NumPy matrix.
    Defaults to THRESHOLD (128) if not specified.
    """
    if threshold is None:
        threshold = THRESHOLD

    matrix = np.array(image)

    binary = matrix < threshold

    return binary


def preprocess_signature(image_path, threshold=None):
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
        resized,
        threshold=threshold
    )

    return {
        "original": original,
        "grayscale": grayscale,
        "resized": resized,
        "binary": binary
    }