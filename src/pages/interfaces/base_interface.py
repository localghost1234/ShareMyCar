# base_interface.py
import tkinter as tk
from tkinter import messagebox

separator_row = "-" * 120

# TODO: combine all loading functions into a single one here
class BaseInterface:
    def __init__(self, root, system, title, subtitle=""):
        self.root = root
        self.system = system
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        tk.Label(self.frame, text=title, font=("Arial", 16)).pack(pady=10)

        # Subtitle label
        tk.Label(self.frame, text=subtitle).pack() if subtitle else None

    def create_scrollable_listbox(self, disable_clicking=True, height=15, width=100, font=("Courier", 10)):
        """
        Creates a scrollable Listbox with vertical and horizontal scrollbars.
        """
        # Frame for the Listbox and scrollbars
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)

        # Listbox
        self.listbox = tk.Listbox(
            self.frame, height=height, width=width,
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

    def load_content(self, get_content, generate_model, header_row, empty_message):
        self.listbox.delete(0, tk.END)  # Clear the listbox

        content = get_content()  # Fetch vehicles
        
        if content:
            self.listbox.insert(tk.END, header_row)  # Insert headers
            self.listbox.insert(tk.END, separator_row)  # Insert a separator line

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
