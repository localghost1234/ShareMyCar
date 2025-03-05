from tkinter import Tk
from src.pages.app import App

if __name__ == "__main__":
    root = Tk()
    root.title("Carsharing Management System")
    app = App(root)
    root.mainloop()