from tkinter import Tk
from src.database.setup import setup_database
from src.pages.app import App

if __name__ == "__main__":
    root = Tk()
    root.geometry("900x720")
    root.title("Carsharing Management System")
    
    setup_database()
    app = App(root)
    
    root.mainloop()