from PIL import Image, ImageChops


def create_difference_image(reference_path, test_path, output_path):
    """
    Compare two signature images and save a visual difference image.

    The two images are converted to grayscale, resized to the same
    dimensions, and compared pixel by pixel.
    """

    # Open both images
    reference = Image.open(reference_path).convert("L")
    test = Image.open(test_path).convert("L")

    # Make both images the same size
    width = min(reference.width, test.width)
    height = min(reference.height, test.height)

    reference = reference.resize((width, height))
    test = test.resize((width, height))

    # Calculate pixel difference
    difference = ImageChops.difference(reference, test)

    # Improve visibility of small differences
    difference = difference.point(
        lambda pixel: 255 if pixel > 20 else 0
    )

    # Save the difference image
    difference.save(output_path)

    return output_path