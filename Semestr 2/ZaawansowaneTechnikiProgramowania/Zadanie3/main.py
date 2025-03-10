import tkinter as tk
from view import ImageView
from presenter import ImagePresenter

if __name__ == "__main__":
    root = tk.Tk()
    presenter = ImagePresenter(ImageView(root, None))
    presenter.view.presenter = presenter  # Circular reference
    root.mainloop()
