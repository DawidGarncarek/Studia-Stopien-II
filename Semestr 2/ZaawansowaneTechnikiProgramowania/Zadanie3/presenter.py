from model import ImageCompressor

class ImagePresenter:
    """
    Prezenter zarządzający logiką aplikacji i interakcją między widokiem a modelem.
    """

    def __init__(self, view):
        """
        Inicjalizuje obiekt ImagePresenter.

        :param view: Obiekt klasy ImageView.
        """
        self.view = view
        self.image_array = None
        self.image_mode = None

    def load_image(self, filepath):
        """
        Wczytuje obraz i wyświetla go w GUI.

        :param filepath: Ścieżka do pliku obrazu.
        """
        if not filepath:
            self.view.show_error("Nie wybrano pliku.")
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
