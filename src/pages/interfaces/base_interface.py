class BaseInterface:
    """
    Base class for creating a graphical user interface with Tkinter.
    This ensures all interfaces are similar and the user can easily navigate around the app.

    Attributes:
        system: Reference to the application's System instance
        frame: The main container frame for the interface
        listbox: The scrollable listbox widget (if created)
    """
    
    def __init__(self, title, subtitle="", system=None):
        """Initializes the interface with a title and optional subtitle.
        
        Args:
            title (str): Main title for the interface
            subtitle (str, optional): Secondary title text
            system (System, optional): Reference to the application's System instance
        """
        self.system = system

        print(title)
        print(subtitle)
        print() if subtitle else None

    def input_loop(self, on_validate_constraints, input_message):
        """Keeps user in an infinite cycle until they give the correct input.
        
        Args:
            on_validate_constraints (Callable): Function to check if the user should remain in the loop or exit.
            input_message (str): Text displayed which should give instructions for user to exit loop.
        """
        action_number = -1
        while on_validate_constraints(action_number):
            try:
                action_number = int(input(input_message))
            except ValueError:
                action_number = -1
        print()
        return action_number

    def load_content(self, headers, get_content, generate_model, empty_message):
        """Loads content and prints it, or shows a message indicating the lackthereof.
        
        Args:
            headers (tuple): Group of strings which will visually represent the names of each column
            get_content (list, callable): List or function that retrieves content to be displayed
            generate_model (callable): Function that formats content for display
            empty_message (str): Message to show when no content is available
        """
        content = get_content if isinstance(get_content, (list, tuple)) else get_content()
        if not content:                                     # Checks if there is available content in DB
            print(empty_message, '\n')                            # Displays 'empty_message' if no data
            return False                                     # Returns a falsy value and stops further code execution
        
        print(self.generate_row(headers))
        for c in content:                                   # Iterates over the extracted DB content (given that the previous condition was false)
            print(generate_model(c))                        # Converts data into the necessary format string and inserts it into the listbox
        
        print()
        return True
    
    def generate_row(self, values):
        """Formats lists of values and turns them into a single string."""
        return "| ".join(f"{v:<16}" for v in values)