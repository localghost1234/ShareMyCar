# base_interface.py
import tkinter as tk
from tkinter import messagebox

class BaseInterface:
    def __init__(self, root, system, title, subtitle):
        self.root = root
        self.system = system
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        tk.Label(self.frame, text=title, font=("Arial", 16)).pack(pady=10)

        # Subtitle label
        tk.Label(self.frame, text=subtitle).pack()

    def create_scrollable_listbox(self, disable_clicking=True, height=15, width=100, font=("Courier", 10)):
        """
        Creates a scrollable Listbox with vertical and horizontal scrollbars.
        Returns the Listbox and its scrollbars.
        """
        # Frame for the Listbox and scrollbars
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)

        # Listbox
        listbox = tk.Listbox(
            self.frame, height=height, width=width,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            font=font
        )

        if disable_clicking:
            # Set selectbackground and selectforeground to match the normal colors
            listbox.config(
                selectbackground=listbox.cget("bg"),  # Match background color
                selectforeground=listbox.cget("fg"),  # Match foreground color
                selectmode=tk.NONE,  # Disable selection
                highlightthickness=0,  # Remove focus highlight border
                activestyle="none"  # Remove the underline/active style
            )

        # Pack elements
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Link scrollbars
        v_scrollbar.config(command=listbox.yview)
        h_scrollbar.config(command=listbox.xview)

        return listbox

    def show_error(self, message):
        """Displays an error message in a messagebox."""
        messagebox.showerror("Error", message)

    def show_info(self, message):
        """Displays an info message in a messagebox."""
        messagebox.showinfo("Info", message)