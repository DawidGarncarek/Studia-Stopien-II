from model import ImageCompressor
import numpy as np

class ImagePresenter:
    """
    Presenter connecting the View and Model for image compression.
    """

    def __init__(self, view):
        self.view = view
        self.image_array = None
        self.image_mode = None

    def load_image(self):
        """Load an image and display it in the UI."""
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp")])
        if not filepath:
            return

        try:
            self.image_array, self.image_mode = ImageCompressor.load_image(filepath)
            self.view.display_image(self.image_array)
        except Exception as e:
            self.view.show_error(str(e))

    def compress_image(self):
        """Compress the image and update the UI."""
        if self.image_array is None:
            self.view.show_error("No image loaded.")
            return

        r = self.view.get_rank()
        if r is None or r <= 0:
            return

        try:
            if self.image_mode == "L":  # Grayscale
                compressed = ImageCompressor.compress_grayscale(self.image_array, r)
            else:  # Color (RGB)
                compressed = ImageCompressor.compress_color(self.image_array, r)

            self.view.display_image(compressed)
        except Exception as e:
            self.view.show_error(str(e))
