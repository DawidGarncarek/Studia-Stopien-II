import numpy as np
from PIL import Image
import os

class ImageCompressor:
    """
    A class to handle image compression using Singular Value Decomposition (SVD).
    """

    @staticmethod
    def load_image(filepath):
        """Load an image and convert it to a numpy array."""
        if not os.path.exists(filepath):
            raise FileNotFoundError("The file does not exist.")

        image = Image.open(filepath)
        return np.array(image), image.mode

    @staticmethod
    def compress_grayscale(image_array, r):
        """Apply SVD-based compression to a grayscale image."""
        try:
            U, S, Vt = np.linalg.svd(image_array, full_matrices=False)
            compressed = np.dot(U[:, :r], np.dot(np.diag(S[:r]), Vt[:r, :]))
            return np.clip(compressed, 0, 255).astype(np.uint8)
        except Exception as e:
            raise ValueError(f"Compression error: {str(e)}")

    @staticmethod
    def compress_color(image_array, r):
        """Apply SVD compression to a color image by handling RGB channels separately."""
        try:
            compressed_channels = []
            for i in range(3):  # RGB channels
                U, S, Vt = np.linalg.svd(image_array[:, :, i], full_matrices=False)
                compressed = np.dot(U[:, :r], np.dot(np.diag(S[:r]), Vt[:r, :]))
                compressed_channels.append(np.clip(compressed, 0, 255).astype(np.uint8))

            return np.dstack(compressed_channels)  # Recombine RGB channels
        except Exception as e:
            raise ValueError(f"Compression error: {str(e)}")
