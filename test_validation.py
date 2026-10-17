import io
import unittest
from PIL import Image
from app import validate_and_load_image
from image_processing import preprocess_signature


class TestValidationAndThreshold(unittest.TestCase):
    def test_empty_file_validation(self):
        empty_stream = io.BytesIO(b"")
        img, err = validate_and_load_image(empty_stream)
        self.assertIsNone(img)
        self.assertIn("empty", err.lower())

    def test_corrupted_file_validation(self):
        corrupt_stream = io.BytesIO(b"Not an image file at all")
        img, err = validate_and_load_image(corrupt_stream)
        self.assertIsNone(img)
        self.assertIn("cannot parse", err.lower())

    def test_small_image_validation(self):
        small_img = Image.new("RGB", (4, 4), (255, 255, 255))
        buf = io.BytesIO()
        small_img.save(buf, format="PNG")
        buf.seek(0)
        img, err = validate_and_load_image(buf)
        self.assertIsNone(img)
        self.assertIn("too small", err.lower())

    def test_valid_image(self):
        valid_img = Image.new("RGB", (100, 100), (255, 255, 255))
        buf = io.BytesIO()
        valid_img.save(buf, format="PNG")
        buf.seek(0)
        img, err = validate_and_load_image(buf)
        self.assertIsNotNone(img)
        self.assertIsNone(err)

    def test_custom_threshold_preprocessing(self):
        # Create an image with pixel values around 150
        img = Image.new("L", (10, 10), 150)
        # With default threshold 128, pixel (150) < 128 is False (no ink)
        prep_default = preprocess_signature(img, threshold=128)
        self.assertFalse(prep_default["binary"].any())
        # With higher threshold 160, pixel (150) < 160 is True (detected as ink)
        prep_custom = preprocess_signature(img, threshold=160)
        self.assertTrue(prep_custom["binary"].all())


if __name__ == "__main__":
    unittest.main()
