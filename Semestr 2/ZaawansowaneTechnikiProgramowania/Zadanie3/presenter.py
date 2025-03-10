from model import ImageCompressor
import os
from tkinter import filedialog


class ImagePresenter:
    """
    Prezenter zarządzający logiką aplikacji i interakcją między widokiem a modelem.
    """

    def __init__(self, view):
        self.view = view
        self.image_array = None
        self.image_mode = None

    def load_image(self):
        """Wczytuje obraz i wyświetla go w GUI."""
        folder_path = os.path.join(os.getcwd(), "Obrazy")

        image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png", ".bmp"))]

        if image_files:
            filepath = os.path.join(folder_path, image_files[0])  
        else:
            filepath = filedialog.askopenfilename(filetypes=[("Obrazy", "*.jpg *.png *.bmp")])

        if not filepath:
            return  

        try:
            self.image_array, self.image_mode = ImageCompressor.load_image(filepath)
            self.view.display_image(self.image_array)
        except Exception as e:
            self.view.show_error(str(e))

    def compress_image(self):
        """Kompresuje obraz i wyświetla wynik."""
        if self.image_array is None:
            self.view.show_error("Najpierw wczytaj obraz.")
            return

        r = self.view.get_rank()
        if r is None or r <= 0:
            return

        try:
            if self.image_mode == "L":  # Skala szarości
                compressed = ImageCompressor.compress_grayscale(self.image_array, r)
            else:  # Kolor RGB
                compressed = ImageCompressor.compress_color(self.image_array, r)

            self.view.display_image(compressed)
        except Exception as e:
            self.view.show_error(str(e))
