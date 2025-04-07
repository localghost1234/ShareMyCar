from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.interface_strings import METRICS                      # Import the METRICS constant, containing strings or configurations for the metrics interface
from reportlab.lib.pagesizes import A4                              # Import the A4 constant from reportlab, defining the standard A4 page size for PDF generation
from reportlab.pdfgen import canvas                                 # Import the canvas class from reportlab for creating and drawing on PDF documents
from datetime import datetime                                       # Import the datetime class for working with dates and times
from copy import deepcopy                                           # Import a module to create a copy of objects like dictionaries to the root
import os                                                           # Import the 'os' class to interact with the PC

class MetricsInterface(BaseInterface):
    """Interface for displaying financial metrics and generating reports.

    This class provides functionality to:
    - View financial metrics (revenue, costs, profit, etc.)
    - Query specific data from database tables
    - Generate comprehensive PDF reports containing:
        - Vehicle inventory
        - Existing bookings
        - Transaction logs

    Attributes:
        on_return_home (Callable): Function used to go back to main menu interface
        system (System): Reference to the application's System instance
    """

    def __init__(self, on_return_home, system):
        """Initialize the metrics interface with financial data display.

        Args:
            system: Reference to the application's System instance
        """
        super().__init__(*METRICS.TITLES, system=system)
        
        metrics = self.system.get_financial_metrics()                                               # Retrieve financial metrics from database
        if not metrics:                                                                             # Checks if content is available
            print(METRICS.EMPTY_MESSAGE)                                                            # Print message for empty content
        else:
            for idx, h in enumerate(METRICS.HEADERS):                                               # Iterates over a list with the info's name, giving out its index and inner value
                print(f"{h}: ", round(metrics[idx], 2))                                             # Displays text with its respective header

        print()                                                                                     # Line break to maintain readability
        action_number = self.input_loop(METRICS.VALIDATOR, METRICS.LOOP_MESSAGE)                    # Activates input loop with its validating conditions and message
        if action_number == 1:                                                                      # Checks if allowed action was chosen
            self.submit_query()                                                                     # Executes module for such action
        elif action_number == 2:                                                                    # Checks if allowed action was chosen
            self.generate_full_report()                                                             # Executes module for such action
        
        on_return_home()                                                                            # Returns to main menu

    def submit_query(self):
        """Allows querying specific info from the database. It allows input in a 'table:column:value' format."""
        print("Input Query")                                                                        # Sets a text in the new frame and positions it
        print("Use '<table>:<column>:<value>' format\n(e.g. vehicles:id:1)")                        # Sets a text in the new frame and positions it
        print("Possible table names: 'vehicles', 'bookings', 'logs'\n")
        try:                                                                                        # Creates a scope for error handling
            query_entry = input('---> ')                                                            # Opens channels to receive user input
            table, column, value = [text.strip() for text in query_entry.split(':')]                # Extract table, column name and value from the user input string (divided into parts by ':' separator)
            results_list = self.system.get_table_row(table, column, value)                          # Extracts database info with specified params
        except:                                                                                     # Handle invalid queries
            print(f"Invalid values, please try again.\n")                                           # Displays error modal
            return                                                                                  # Stops further code execution

        if not results_list:                                                                        # Handle no results
            print("No results found.\n")                                                            # Displays text when no data is found
            return                                                                                  # Stops further code execution

        print(f"{len(results_list)} results found:\n")                                              # Displays and positions the number of results found
        print(self.generate_row(results_list[0].keys()))                                            # Takes the first value of results_list, extracts its keys, and turns them into a single text line

        for item in results_list:                                                                   # Iterate over the list with the query results
            print(self.generate_row(str(v) for v in item.values()))                                 # Extract the values of every dictionary in the list, turns them into a single string and prints them

        print()                                                                                     # Line break to maintain readability

    def generate_full_report(self):
        """Generate a comprehensive PDF report containing:
            - Vehicle inventory
            - Booking records
            - Transaction logs
        """
        current_datetime = datetime.now()                                               # Get an object with the current date and time
        directory = f"{os.getcwd()}\\reports"                                           # Sets a string with the current working directory, and adds a new dir where the reports shall be stored
        os.makedirs(directory, exist_ok=True)                                           # Checks if the directory exists, and creates it if it does not
        filename = f"FullReport_{current_datetime.strftime('%Y-%m-%d_%H%M%S')}.pdf"     # Sets a string to be used as the name of the file, with the current time
        file_path = f"{directory}\\{filename}"                                          # Sets the complete path where the file will be stored

        pdf = canvas.Canvas(file_path, pagesize=A4)                                     # Create a PDF file object to manipulate
        _, height = A4                                                                  # Obtain a variable with the PDF format's height
        y_position = height - 40                                                        # Start position for content
        font_size = 6                                                                   # Define text size

        pdf.setFont("Helvetica-Bold", font_size * 1.5)                                                          # Set top text's font
        pdf.drawString(200, y_position, f"Full Report - {current_datetime.strftime('%Y-%m-%d_%H:%M:%S')}")      # Write the title's string on top of the file

        x_position = 50                                                                              # Adjust horizontal position
        y_position = height - 50                                                                     # Adjust vertical position for further text strings
        pdf.setFont("Helvetica", font_size)                                                          # Define text font and size for PDF object

        def draw_table(title, data):
            """Draw a formatted table in the PDF document.
            
            Args:
                headers (list): Column headers for the table
                data (dictionary): List of rows to display in the table
            """
            nonlocal y_position                                                       # Since variable 'y_position' is set outside of this scope, we need to remind the function to use its outter value
            pdf.drawString(x_position, y_position, title)                             # Writes text to PDF with the displayed table's name
            y_position -= font_size * 1.5                                             # Lowers the vertical position of the pointer, in accordance to the row's text size
            
            if not data:                                                              # Checks if content is available
                pdf.drawString(x_position, y_position, 'EMPTY')                       # If no content is found, a string is displayed instead of a table
                y_position -= font_size * 2                                           # Lowers the vertical position of the pointer, in accordance to the row's text size
                return                                                                # Stops further code execution
     
            headers = [str(key).upper() for key in list(data[0].keys())]                                                    # Gets a list of the column names, turns them into strings and capitalizes them
            rows = [[str(value) for value in list(row.values())] for row in data]                                           # Gets a list of the values of every object in 'data' and turns them into strings for easier handling
            col_widths = [w * font_size * 0.8 for w in [max(len(item) for item in col) for col in zip(headers, *rows)]]     # Gets the max width for each column by finding the longest string length in headers and data and changes the scale of each width dynamically and returns the results
       
            x_pos_headers = x_position                                                                                      # TODO: Improve this -- creates a new variable with the same value, but can lead to errors
            for i, h in enumerate(headers):                                                                                 # Takes the index and inner value of the 'headers' list
                pdf.drawString(x_pos_headers, y_position, h)                                                                # Writes the column names (headers) at the indicated position of the PDF
                x_pos_headers += col_widths[i]                                                                              # Depending on the amount of columns, the horizontal position is moved
            
            y_position -= font_size * 1.25                                                                # Lowers the vertical position of the pointer, in accordance to the row's text size
            for row in rows:                                                                              # Iterate over the list of database content
                x_pos_cell = x_position                                                                   # TODO: Improve this -- creates a new variable with the same value, but can lead to errors
                for i, cell in enumerate(row):                                                            # Extract each piece of information from the row's list and their index
                    pdf.drawString(x_pos_cell, y_position, str(cell))                                     # Writes the information to the PDF, aligned with its corresponding column
                    x_pos_cell += col_widths[i]                                                           # Moves the PDF object's pointer to the next column's horizontal position
                y_position -= font_size * 1.25                                                            # Move the vertical pointer to the next row's position, in accordance to the row's text size
                if y_position < 50:                                                                       # Checks if vertical position is close to the end of the page
                    pdf.showPage()                                                                        # Closes current page and if needed, starts a new one
                    y_position = height - 50                                                              # Resets the vertical pointer at the top of the page's size
            
            y_position -= font_size * 2.5                                                                 # Lowers the vertical position of the pointer, in accordance to the row's text size

        draw_table("Vehicles:", deepcopy(self.system.vehicles))                                    # Uses table information to generate, format, and print the PDF's contents
        draw_table("Bookings:", deepcopy(self.system.bookings))                                    # Uses table information to generate, format, and print the PDF's contents
        draw_table("Logs:", deepcopy(self.system.logs))                                            # Uses table information to generate, format, and print the PDF's contents
        
        pdf.save()                                                                       # Generate the final PDF file in the previously accorded path
        print(f"Report saved as {file_path}\n")                                          # Show a success message on the console with the new file's path