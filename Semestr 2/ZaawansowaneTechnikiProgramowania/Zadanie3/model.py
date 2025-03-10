import numpy as np
from PIL import Image
import os

class ImageCompressor:
    """
    Klasa do obsługi kompresji obrazów za pomocą dekompozycji według wartości osobliwych (SVD).
    """

    @staticmethod
    def load_image(filepath):
        """Wczytuje obraz i konwertuje go do postaci macierzy NumPy."""
        if not os.path.exists(filepath):
            raise FileNotFoundError("Plik nie istnieje.")

        image = Image.open(filepath)
        return np.array(image), image.mode

    @staticmethod
    def compress_grayscale(image_array, r):
        """Kompresja obrazu w skali szarości za pomocą SVD."""
        try:
            U, S, Vt = np.linalg.svd(image_array, full_matrices=False)

            r = min(r, len(S))         
            compressed = np.dot(U[:, :r], np.dot(np.diag(S[:r]), Vt[:r, :]))
            return np.clip(compressed, 0, 255).astype(np.uint8)
        except Exception as e:
            raise ValueError(f"Błąd kompresji: {str(e)}")

    @staticmethod
    def compress_color(image_array, r):
        """Kompresja obrazu kolorowego (RGB) za pomocą SVD."""
        try:
            compressed_channels = []
            for i in range(3):  
                U, S, Vt = np.linalg.svd(image_array[:, :, i], full_matrices=False)

                r = min(r, len(S)) 
                compressed = np.dot(U[:, :r], np.dot(np.diag(S[:r]), Vt[:r, :]))
                compressed_channels.append(np.clip(compressed, 0, 255).astype(np.uint8))

            return np.dstack(compressed_channels) 
        except Exception as e:
            raise ValueError(f"Błąd kompresji: {str(e)}")
