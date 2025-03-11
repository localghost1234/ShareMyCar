# base_interface.py
import tkinter as tk
from tkinter import messagebox
from src.misc.utilities import generate_header_row

class BaseInterface:
    def __init__(self, root, system, title, subtitle=""):
        self.root = root
        self.system = system
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        tk.Label(self.frame, text=title, font=("Arial", 18)).pack(pady=10)

        # Subtitle label
        tk.Label(self.frame, text=subtitle, font=("Arial", 12)).pack() if subtitle else None

    def create_scrollable_listbox(self, headers=(), disable_clicking=True, font=("Courier", 12)):
        """
        Creates a scrollable Listbox with vertical and horizontal scrollbars.
        """
        tk.Label(self.frame, text=generate_header_row(headers)).pack() if headers else None  # Insert headers

        # Frame for the Listbox and scrollbars
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)

        # Listbox
        self.listbox = tk.Listbox(
            self.frame,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            font=font
        )

        if disable_clicking:
            # Set selectbackground and selectforeground to match the normal colors
            self.listbox.config(
                selectbackground=self.listbox.cget("bg"),  # Match background color
                selectforeground=self.listbox.cget("fg"),  # Match foreground color
                selectmode=tk.NONE,  # Disable selection
                highlightthickness=0,  # Remove focus highlight border
                activestyle="none"  # Remove the underline/active style
            )

        # Pack elements
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Link scrollbars
        v_scrollbar.config(command=self.listbox.yview)
        h_scrollbar.config(command=self.listbox.xview)

    def load_content(self, get_content, generate_model, empty_message):
        self.listbox.delete(0, tk.END)  # Clear the listbox

        content = get_content()  # Fetch vehicles
        
        if content:
            for c in content:
                model = generate_model(c)
                self.listbox.insert(tk.END, model)
        else:
            self.listbox.insert(tk.END, empty_message)

    def show_info(self, message):
        """Displays an info message in a messagebox."""
        messagebox.showinfo("Info", message)

    def show_error(self, message):
        """Displays an error message in a messagebox."""
        messagebox.showerror("Error", message)
