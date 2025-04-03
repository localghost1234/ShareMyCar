from src.misc.utilities import generate_header_row      # Import the generate_header_row function, which returns a formatted string to use as column names

class BaseInterface:
    """
    Base class for creating a graphical user interface with Tkinter.
    This ensures all interfaces are similar and the user can easily navigate around the app.

    Attributes:
        system: Reference to the application's System instance
        frame: The main container frame for the interface
        listbox: The scrollable listbox widget (if created)
    """
    
    def __init__(self, system, title, subtitle=""):
        """Initializes the interface with a title and optional subtitle.
        
        Args:
            system: Reference to the application's System instance
            title (str): Main title for the interface
            subtitle (str, optional): Secondary title text
        """
        self.system = system

        print(title)
        print(subtitle)
        print()


    def load_content(self, headers, get_content, generate_model, empty_message):
        """Loads content into the Listbox based on provided data retrieval functions.
        
        Args:
            get_content (callable): Function that retrieves content to display
            generate_model (callable): Function that formats content for display
            empty_message (str): Message to show when no content is available
        """
        content = get_content()                             # Fetch data from system's function
        
        if not content:                                     # Checks if there is available content in DB
            print(empty_message)                            # Displays 'empty_message' if no data
            return                                     # Returns a falsy value and stops further code execution

        print(generate_header_row(headers))
        
        for idx, c in enumerate(content):                                   # Iterates over the extracted DB content (given that the previous condition was false)
            print(generate_model(idx + 1, c))                        # Converts data into the necessary format string and inserts it into the listbox