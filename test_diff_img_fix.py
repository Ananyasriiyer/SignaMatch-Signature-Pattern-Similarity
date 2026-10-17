import io
import os
import unittest
from PIL import Image

from difference_analysis import create_difference_image


class TestDiffImgSave(unittest.TestCase):
    def setUp(self):
        self.ref_path = "Signatures/reference/signature1.jpeg"
        self.test_path = "Signatures/test/signature2.jpeg"
        self.out_path = "results/signature_difference.png"

    def test_difference_image_with_output_path(self):
        # 1. Generate difference image with output path
        diff_res = create_difference_image(
            self.ref_path,
            self.test_path,
            output_path=self.out_path
        )
        self.assertTrue(os.path.exists(self.out_path))

        # 2. Check conversion logic from app.py
        if isinstance(diff_res, str):
            diff_img = Image.open(diff_res)
        else:
            diff_img = diff_res

        self.assertIsInstance(diff_img, Image.Image)

        # 3. Test saving to in-memory buffer (the exact line that previously failed)
        buf = io.BytesIO()
        diff_img.save(buf, format="PNG")
        val = buf.getvalue()

        # PNG magic bytes: \x89PNG\r\n\x1a\n
        self.assertTrue(len(val) > 0)
        self.assertTrue(val.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_difference_image_without_output_path(self):
        # When called without output path, should return PIL Image directly
        diff_res = create_difference_image(self.ref_path, self.test_path)
        self.assertIsInstance(diff_res, Image.Image)

        buf = io.BytesIO()
        diff_res.save(buf, format="PNG")
        val = buf.getvalue()
        self.assertTrue(len(val) > 0)
        self.assertTrue(val.startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
