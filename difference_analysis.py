import os
from PIL import Image, ImageChops
from image_processing import load_image, convert_to_grayscale


def create_difference_image(reference_path, test_path, output_path=None):
    """
    Compare two signature images and generate/save a visual difference image.

    The two images are converted to grayscale, resized to the same
    dimensions, and compared pixel by pixel.
    Supports file paths, file streams, or existing PIL Images.
    If output_path is provided, the image is saved to disk and output_path is returned.
    If output_path is None, the PIL difference image is returned directly.
    """

    # Open both images using robust loader
    ref_img = load_image(reference_path)
    test_img = load_image(test_path)

    # Convert to grayscale with proper alpha/transparency handling
    reference = convert_to_grayscale(ref_img)
    test = convert_to_grayscale(test_img)

    # Make both images the same size (matching minimum dimensions)
    width = min(reference.width, test.width)
    height = min(reference.height, test.height)

    # Prevent zero-size edge case
    width = max(width, 1)
    height = max(height, 1)

    reference = reference.resize((width, height))
    test = test.resize((width, height))

    # Calculate pixel difference
    difference = ImageChops.difference(reference, test)

    # Improve visibility of small differences
    difference = difference.point(
        lambda pixel: 255 if pixel > 20 else 0
    )

    # Save the difference image if output_path is specified
    if output_path:
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        difference.save(output_path)
        return output_path

    return difference