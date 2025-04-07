class BaseInterface:
    """Base class for standardizing user experience.
    This ensures all or most interfaces share similar features and the user can easily navigate around the app.
    """
    
    def __init__(self, title, subtitle="", system=None):
        """Initializes the interface with a title and optional subtitle.
        
        Args:
            title (str): Main title for the interface
            subtitle (str, optional): Secondary title text
            system (System, optional): Reference to the application's System instance
        """
        self.system = system                    # Pass system param to keep it in interface at all times
        print(title)                            # Print upper interface text
        print(subtitle)                         # Print lower interface text
        print() if subtitle else None           # Print line break, if a subtitle was given

    def input_loop(self, on_validate_constraints, input_message):
        """Keeps user in an infinite cycle until they give the correct input.
        
        Args:
            on_validate_constraints (Callable): Function to check if the user should remain in the loop or exit.
            input_message (str): Text displayed; should give instructions on how to exit loop.
        """
        action_number = -1                              # Initialize number's variable
        while on_validate_constraints(action_number):   # Creates an infinite loop, only broken when conditions provided by the interface are met
            try:                                                # Creates a scope to enclose any input given by the user in case something disagreeable is entered
                action_number = abs(int(input(input_message)))  # Opens channel for user to interace with the app, turn it into an int (or raise an error if not possible), and if anything, turn it into an absolute number
            except ValueError:                                  # If user input is cannot be turned into a number, we skip the previous code to this line
                action_number = -1                              # Variable gets reset to non-acceptable value, maintaining user in the loop
        print()                                   # Prints a line break to keep understandability
        return action_number                      # Return clean user input

    def load_content(self, headers, get_content, generate_model, empty_message):
        """Loads content and prints it, or shows a message indicating the lackthereof.
        
        Args:
            headers (tuple): Group of strings which will visually represent the names of each column
            get_content (list, callable): List or function that retrieves content to be displayed
            generate_model (callable): Function that formats content for display
            empty_message (str): Message to show when no content is available
        """
        content = get_content if isinstance(get_content, (list, tuple)) else get_content()  # Content may come in the form of iterable or function, so we check and obtain it from either one
        if not content:                                                                     # Checks if there is available content in DB
            print(empty_message, '\n')                                                      # Displays 'empty_message' if no data
            return False                                                                    # Returns False and stops further code execution
        
        print(self.generate_row(headers))                   # Creates and prints into console a string of the column names
        for c in content:                                   # Iterates over the extracted DB content
            print(generate_model(c))                        # Converts data into the necessary format string and prints it
        
        print()                                             # Line break to keep understandibility
        return True                                         # Return True to indicate success
    
    def generate_row(self, values):
        """Formats lists of values and turns them into a single string."""
        return "| ".join(f"{v:<16}" for v in values)