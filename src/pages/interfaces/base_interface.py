import tkinter as tk
from tkinter import messagebox
from src.misc.utilities import generate_header_row

class BaseInterface:
    """
        Base class for creating a graphical user interface with Tkinter.
        This ensures all interfaces are similar and the user can easily navigate around the app.
    """
    
    def __init__(self, root, system, title, subtitle=""):
        """Initializes the interface with a title and optional subtitle."""
        self.root = root  # We take the 'root' (main tkinter Frame) to keep every new object inside the window
        self.system = system  # We reference the original System class (which orchestrates the DB and its usage)
        self.frame = tk.Frame(root)  # We generate an inner window where each interface's elements will remain until erased
        self.frame.pack(fill=tk.BOTH, expand=True)  # We fill up the window's space with our new Frame

        tk.Label(self.frame, text=title, font=("Arial", 18)).pack(pady=15)  # We add a string with whatever title we prefer and give it some space from other vertical elements
        tk.Label(self.frame, text=subtitle, font=("Arial", 14)).pack(pady=7) if subtitle else None  # An optional string, for extra information, in case some element is given

    def create_scrollable_listbox(self, headers=(), disable_clicking=True, font=("Courier", 10)):
        """
            Creates a scrollable Listbox object, which displays the given information.
            It is an optional feature, and relies on its sister function load_content()
            to start/reset all the listbox's values.
        """
        if headers:
            tk.Label(self.frame, text=generate_header_row(headers)).pack()  # Insert headers
        
        self.frame.pack(fill=tk.BOTH, expand=True)  # Ensure frame fills the window

        v_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)  # Vertical scrollbar
        h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)  # Horizontal scrollbar

        self.listbox = tk.Listbox(
            self.frame,
            yscrollcommand=v_scrollbar.set,  # Link vertical scrollbar
            xscrollcommand=h_scrollbar.set,  # Link horizontal scrollbar
            font=font
        )

        if disable_clicking:
            self.listbox.config(
                selectbackground=self.listbox.cget("bg"),  # Prevent selection highlight
                selectforeground=self.listbox.cget("fg"),  # Keep text color unchanged
                selectmode=tk.NONE,  # Disable selection mode
                highlightthickness=0,  # Remove focus border
                activestyle="none"  # Disable underline/active style
            )

        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Place vertical scrollbar
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)  # Place horizontal scrollbar
        self.listbox.pack(fill=tk.BOTH, expand=True)  # Place listbox

        v_scrollbar.config(command=self.listbox.yview)  # Link scrollbar to listbox
        h_scrollbar.config(command=self.listbox.xview)  # Link scrollbar to listbox

    def load_content(self, get_content, generate_model, empty_message):
        """Loads content into the Listbox based on provided data retrieval functions."""
        self.listbox.delete(0, tk.END)  # Clear existing listbox content

        content = get_content()  # Fetch data
        
        if content:
            for c in content:
                model = generate_model(c)  # Convert data into display format
                self.listbox.insert(tk.END, model)  # Insert into listbox
        else:
            self.listbox.insert(tk.END, empty_message)  # Display empty message if no data

    def show_info(self, message):
        """Displays an informational message in a popup window."""
        messagebox.showinfo("Info", message)

    def show_error(self, message):
        """Displays an error message in a popup window."""
        messagebox.showerror("Error", message)