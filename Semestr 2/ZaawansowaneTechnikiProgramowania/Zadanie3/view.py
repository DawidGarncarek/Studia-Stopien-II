import tkinter as tk
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk

class ImageView:
    """
    Graficzny interfejs użytkownika do aplikacji kompresji obrazów.
    """

    def __init__(self, root, presenter):
        """
        Inicjalizuje interfejs użytkownika.

        :param root: Główne okno aplikacji.
        :param presenter: Obiekt klasy ImagePresenter zarządzający logiką aplikacji.
        """
        self.presenter = presenter
        self.root = root
        self.root.title("Kompresja Obrazów (SVD)")
        self.root.geometry("800x600")

        # Folder, w którym są obrazy
        self.folder_path = os.path.join(os.getcwd(), "Obrazy")
        self.image_files = self.get_image_files()

        # Lista rozwijana do wyboru pliku
        self.file_label = tk.Label(root, text="Wybierz plik:")
        self.file_label.pack()

        self.file_combobox = ttk.Combobox(root, values=self.image_files)
        self.file_combobox.pack()
        if self.image_files:
            self.file_combobox.set(self.image_files[0])  # Domyślnie wybierz pierwszy plik

        # Przycisk do wczytania obrazu
        self.load_button = tk.Button(root, text="Wczytaj Obraz", command=self.load_selected_image)
        self.load_button.pack(pady=10)

        # Pole do wpisania wartości r
        self.rank_label = tk.Label(root, text="Liczba wartości osobliwych (r):")
        self.rank_label.pack()
        self.rank_entry = ttk.Entry(root)
        self.rank_entry.pack()

        # Przycisk do kompresji
        self.compress_button = tk.Button(root, text="Kompresuj Obraz", command=self.presenter.compress_image if self.presenter else None)
        self.compress_button.pack(pady=10)

        # Obszar na wyświetlanie obrazów
        self.image_canvas = tk.Canvas(root, width=500, height=400)
        self.image_canvas.pack()

    def set_presenter(self, presenter):
        """Ustawia prezentera i przypisuje funkcje do przycisków."""
        self.presenter = presenter
        self.load_button.config(command=self.load_selected_image)  
        self.compress_button.config(command=self.presenter.compress_image)  

    def get_image_files(self):
        """
        Pobiera listę dostępnych obrazów w folderze 'Obrazy'.

        :return: Lista nazw plików obrazów.
        """
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)  # Tworzymy folder, jeśli nie istnieje
        return [f for f in os.listdir(self.folder_path) if f.lower().endswith((".jpg", ".png", ".bmp"))]

    def load_selected_image(self):
        """Wczytuje obraz wybrany w comboboxie."""
        if not self.presenter:
            return

        selected_file = self.file_combobox.get()
        filepath = os.path.join(self.folder_path, selected_file)

        try:
            self.presenter.load_image(filepath)
        except Exception as e:
            self.show_error(str(e))

    def display_image(self, image_array):
        """
        Wyświetla obraz w oknie aplikacji.

        :param image_array: Macierz NumPy reprezentująca obraz.
        """
        img = Image.fromarray(image_array)
        img.thumbnail((500, 400))
        img = ImageTk.PhotoImage(img)

        self.image_canvas.create_image(250, 200, image=img)
        self.image_canvas.image = img  # Zatrzymujemy referencję do obrazu

    def get_rank(self):
        """
        Pobiera wartość r od użytkownika.

        :return: Liczba wartości osobliwych r lub None, jeśli podano niepoprawną wartość.
        """
        try:
            r = int(self.rank_entry.get())
            if r <= 0:
                raise ValueError
            return r
        except ValueError:
            self.show_error("Podaj poprawną liczbę całkowitą większą od 0.")
            return None

    def show_error(self, message):
        """
        Wyświetla komunikat błędu.

        :param message: Tekst komunikatu błędu.
        """
        messagebox.showerror("Błąd", message)
