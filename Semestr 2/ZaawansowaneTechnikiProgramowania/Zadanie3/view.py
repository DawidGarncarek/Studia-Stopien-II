import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import numpy as np

class ImageView:
    """
    GUI for Image Compression Application.
    """

    def __init__(self, root, presenter):
        self.presenter = presenter
        self.root = root
        self.root.title("Image Compression (SVD)")
        self.root.geometry("800x600")

        # File selection button
        self.load_button = tk.Button(root, text="Load Image", command=self.presenter.load_image)
        self.load_button.pack(pady=10)

        # Entry for SVD rank
        self.rank_label = tk.Label(root, text="SVD Rank (r):")
        self.rank_label.pack()
        self.rank_entry = ttk.Entry(root)
        self.rank_entry.pack()

        # Compression button
        self.compress_button = tk.Button(root, text="Compress Image", command=self.presenter.compress_image)
        self.compress_button.pack(pady=10)

        # Canvas for displaying images
        self.image_canvas = tk.Canvas(root, width=500, height=400)
        self.image_canvas.pack()

    def display_image(self, image_array):
        """Display the image on the tkinter canvas."""
        img = Image.fromarray(image_array)
        img.thumbnail((500, 400))
        img = ImageTk.PhotoImage(img)

        self.image_canvas.create_image(250, 200, image=img)
        self.image_canvas.image = img  # Keep a reference

    def get_rank(self):
        """Get the user input for SVD rank."""
        try:
            return int(self.rank_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for rank.")
            return None

    def show_error(self, message):
        """Display an error message."""
        messagebox.showerror("Error", message)
