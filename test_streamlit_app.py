import os
import unittest
from PIL import Image
import numpy as np

from image_processing import preprocess_signature, load_image, convert_to_grayscale
from fingerprint import generate_fingerprint
from lcs import calculate_lcs_length, calculate_similarity, compare_fingerprints, get_lcs_subsequence
from similarity import create_similarity_result, classify_similarity
from difference_analysis import create_difference_image
from explainable_result import explain_similarity
from comparison_history import save_comparison, load_history, clear_history


class TestSignaMatchPipeline(unittest.TestCase):
    def setUp(self):
        self.ref_path = "Signatures/reference/signature1.jpeg"
        self.test_path = "Signatures/test/signature2.jpeg"

    def test_sample_files_exist(self):
        self.assertTrue(os.path.exists(self.ref_path), "Reference signature file missing")
        self.assertTrue(os.path.exists(self.test_path), "Test signature file missing")

    def test_image_preprocessing(self):
        prep = preprocess_signature(self.ref_path)
        self.assertIn("original", prep)
        self.assertIn("grayscale", prep)
        self.assertIn("resized", prep)
        self.assertIn("binary", prep)
        self.assertEqual(prep["resized"].size, (64, 64))
        self.assertEqual(prep["binary"].shape, (64, 64))

    def test_fingerprint_generation(self):
        prep = preprocess_signature(self.ref_path)
        fp_data = generate_fingerprint(prep["binary"])
        self.assertIn("fingerprint", fp_data)
        fp = fp_data["fingerprint"]
        self.assertEqual(len(fp), 16)
        # Check all characters are valid hexadecimal
        for c in fp:
            self.assertIn(c, "0123456789ABCDEF")

    def test_lcs_identical_strings(self):
        s1 = "6656642222223333"
        s2 = "6656642222223333"
        lcs_len = calculate_lcs_length(s1, s2)
        sim = calculate_similarity(s1, s2)
        subseq = get_lcs_subsequence(s1, s2)
        self.assertEqual(lcs_len, 16)
        self.assertEqual(sim, 100.0)
        self.assertEqual(subseq, s1)

    def test_lcs_and_subsequence(self):
        s1 = "6656642222223333"
        s2 = "7653224222211111"
        lcs_len = calculate_lcs_length(s1, s2)
        subseq = get_lcs_subsequence(s1, s2)
        self.assertEqual(len(subseq), lcs_len)
        self.assertEqual(lcs_len, 8)
        comp = compare_fingerprints(s1, s2)
        self.assertEqual(comp["lcs_length"], 8)
        self.assertEqual(comp["similarity"], 50.0)

    def test_similarity_classification(self):
        self.assertEqual(classify_similarity(95), "Very High Similarity")
        self.assertEqual(classify_similarity(80), "High Similarity")
        self.assertEqual(classify_similarity(60), "Moderate Similarity")
        self.assertEqual(classify_similarity(30), "Low Similarity")

    def test_difference_image_creation(self):
        diff = create_difference_image(self.ref_path, self.test_path)
        self.assertIsInstance(diff, Image.Image)
        self.assertEqual(diff.mode, "L")

    def test_transparency_handling(self):
        # Create a transparent RGBA image with a dark circle
        img = Image.new("RGBA", (100, 100), (0, 0, 0, 0)) # transparent background
        gray = convert_to_grayscale(img)
        # Background should be pure white (255) not black (0)
        self.assertEqual(gray.getpixel((0, 0)), 255)

    def test_history_logging(self):
        save_comparison("ref_test.png", "test_test.png", 85.5, "High Similarity")
        hist = load_history()
        self.assertTrue(len(hist) > 0)
        last = hist[-1]
        self.assertEqual(last["Reference Signature"], "ref_test.png")
        self.assertEqual(last["Test Signature"], "test_test.png")
        self.assertEqual(last["Similarity Percentage"], "85.50")


if __name__ == "__main__":
    unittest.main()
