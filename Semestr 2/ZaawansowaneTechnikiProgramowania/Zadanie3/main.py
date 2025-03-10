import tkinter as tk
from view import ImageView
from presenter import ImagePresenter

if __name__ == "__main__":
    root = tk.Tk()
    view = ImageView(root, None)  
    presenter = ImagePresenter(view)
    view.set_presenter(presenter)
    root.mainloop()
