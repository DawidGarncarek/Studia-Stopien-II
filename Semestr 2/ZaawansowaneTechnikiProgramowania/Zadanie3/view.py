import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class ImageView:
    """
    Graficzny interfejs użytkownika do aplikacji kompresji obrazów.
    """

    def __init__(self, root, presenter):
        self.presenter = presenter  # Może być None, ale to naprawimy w `main.py`
        self.root = root
        self.root.title("Kompresja Obrazów (SVD)")
        self.root.geometry("800x600")

        # Przycisk do wczytania pliku (na razie nie podpinamy akcji, bo presenter może być None)
        self.load_button = tk.Button(root, text="Wczytaj Obraz")
        self.load_button.pack(pady=10)

        # Pole do wpisania wartości r
        self.rank_label = tk.Label(root, text="Liczba wartości osobliwych (r):")
        self.rank_label.pack()
        self.rank_entry = ttk.Entry(root)
        self.rank_entry.pack()

        # Przycisk do kompresji (również na razie bez akcji)
        self.compress_button = tk.Button(root, text="Kompresuj Obraz")
        self.compress_button.pack(pady=10)

        # Obszar na wyświetlanie obrazów
        self.image_canvas = tk.Canvas(root, width=500, height=400)
        self.image_canvas.pack()

    def set_presenter(self, presenter):
        """Ustawia prezentera i dopiero wtedy przypisuje funkcje do przycisków."""
        self.presenter = presenter
        self.load_button.config(command=self.presenter.load_image)
        self.compress_button.config(command=self.presenter.compress_image)

    def display_image(self, image_array):
        """Wyświetla obraz w oknie aplikacji."""
        img = Image.fromarray(image_array)
        img.thumbnail((500, 400))
        img = ImageTk.PhotoImage(img)

        self.image_canvas.create_image(250, 200, image=img)
        self.image_canvas.image = img  

    def get_rank(self):
        """Pobiera wartość r od użytkownika."""
        try:
            return int(self.rank_entry.get())
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną liczbę całkowitą.")
            return None

    def show_error(self, message):
        """Wyświetla komunikat błędu."""
        messagebox.showerror("Błąd", message)
