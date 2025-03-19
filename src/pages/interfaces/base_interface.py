import tkinter as tk                                    # Import the tkinter library for creating the GUI, aliased as 'tk' for convenience
from tkinter import messagebox                          # Import the messagebox module from tkinter for displaying pop-up messages (e.g., alerts, warnings)
from src.misc.utilities import generate_header_row      # Import the generate_header_row function, which returns a formatted string to use as column names

class BaseInterface:
    """
        Base class for creating a graphical user interface with Tkinter.
        This ensures all interfaces are similar and the user can easily navigate around the app.
    """
    
    def __init__(self, root, system, title, subtitle=""):
        """Initializes the interface with a title and optional subtitle."""
        self.system = system                                                                        # We reference the original System class (which orchestrates the DB and its usage)
        self.frame = tk.Frame(root)                                                                 # We generate an inner window where each interface's elements will remain until erased
        self.frame.pack(fill=tk.BOTH, expand=True)                                                  # We fill up the window's space with our new Frame

        tk.Label(self.frame, text=title, font=("Arial", 18)).pack(pady=15)                          # We add a string with whatever title we prefer and give it some space from other vertical elements
        tk.Label(self.frame, text=subtitle, font=("Arial", 14)).pack(pady=7) if subtitle else None  # An optional string, for extra information, in case some element is given

    def create_scrollable_listbox(self, headers=(), disable_clicking=True, font=("Courier", 10)):
        """
            Creates a scrollable Listbox object, which displays the given information.
            It is an optional feature, and relies on its sister function load_content()
            to start/reset all the listbox's values.
        """
        if headers:
            tk.Label(self.frame, text=generate_header_row(headers)).pack()  # If 'headers' has any values in it, they get displayed on top of the listbox
        
        self.frame.pack(fill=tk.BOTH, expand=True)                          # Ensure frame fills the window

        v_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)          # Initializes vertical scrollbar
        h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)        # Initializes horizontal scrollbar

        self.listbox = tk.Listbox(                                          # Initializes listbox object, and adds its reference to the class object
            self.frame,                                                     # Indicates the parent Frame, to keep the content from spilling outside the visual scope
            yscrollcommand=v_scrollbar.set,                                 # Link vertical scrollbar to listbox
            xscrollcommand=h_scrollbar.set,                                 # Link horizontal scrollbar to listbox
            font=font
        )

        if disable_clicking:                                                # Checks whether content is to be clicked on
            self.listbox.config(                                            # Opens Listbox configuration module
                selectbackground=self.listbox.cget("bg"),                   # Prevent selection highlight
                selectforeground=self.listbox.cget("fg"),                   # Keep text color unchanged
                selectmode=tk.NONE,                                         # Disable selection mode
                highlightthickness=0,                                       # Remove focus border
                activestyle="none",                                         # Disable underline/active style
            )

        v_scrollbar.config(command=self.listbox.yview)                      # Link vertical scrollbar to Listbox
        h_scrollbar.config(command=self.listbox.xview)                      # Link horizontal scrollbar to Listbox

        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)                          # Positions vertical scrollbar within Frame
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)                         # Positions horizontal scrollbar within Frame
        self.listbox.pack(fill=tk.BOTH, expand=True)                        # Positions Listbox and expands it within Frame

    def load_content(self, get_content, generate_model, empty_message):
        """Loads content into the Listbox based on provided data retrieval functions."""
        self.listbox.delete(0, tk.END)                      # Clear existing listbox content
        content = get_content()                             # Fetch data from system's function
        
        if not content:                                     # Checks if there is available content in DB
            self.listbox.insert(tk.END, empty_message)      # Displays 'empty_message' if no data
            return None                                     # Returns a falsy value, in case something is expected
        
        for c in content:                                   # Iterates over the extracted DB content (given that the previous condition was false)
            self.listbox.insert(tk.END, generate_model(c))  # Converts data into the necessary format string and inserts it into the listbox

    def show_info(self, message):
        """Displays an informational message in a popup window."""
        messagebox.showinfo("Info", message)

    def show_error(self, message):
        """Displays an error message in a popup window."""
        messagebox.showerror("Error", message)