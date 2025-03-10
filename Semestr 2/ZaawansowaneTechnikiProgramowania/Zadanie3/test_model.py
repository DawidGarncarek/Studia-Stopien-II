import unittest
import numpy as np
from model import ImageCompressor

class TestImageCompressor(unittest.TestCase):

    def test_grayscale_compression(self):
        img = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        compressed = ImageCompressor.compress_grayscale(img, 10)
        self.assertEqual(compressed.shape, img.shape)

    def test_color_compression(self):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        compressed = ImageCompressor.compress_color(img, 10)
        self.assertEqual(compressed.shape, img.shape)

if __name__ == "__main__":
    unittest.main()
