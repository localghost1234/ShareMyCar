from src.pages.interfaces.base_interface import BaseInterface   # Import the BaseInterface class, a parent class providing common functionality for other interfaces
#from fpdf import pdf
from reportlab.lib.pagesizes import A4                          # Import the A4 constant from reportlab, defining the standard A4 page size for PDF generation
from reportlab.pdfgen import canvas                             # Import the canvas class from reportlab for creating and drawing on PDF documents
from datetime import datetime                                   # Import the datetime class for working with dates and times
from src.misc.strings import METRICS                            # Import the METRICS constant, containing strings or configurations for the metrics interface
from src.misc.utilities import input_loop
import os

class MetricsInterface(BaseInterface):
    """Interface for displaying financial metrics and generating reports.

    This class provides functionality to:
    - View financial metrics (revenue, costs, profit, etc.)
    - Query specific data from database tables
    - Generate comprehensive PDF reports containing:
        - Vehicle inventory
        - Booking records
        - Transaction logs

    Attributes:
        system: Reference to the application's System instance
    """

    def __init__(self, on_switch_interface, system):
        """Initialize the metrics interface with financial data display.

        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, *METRICS.TITLES)                                                          # Initializes 'BaseInterface' with the pre-defined TITLES strings

        metrics = ()                                                                                             # Initializes tuple with the metrics info
        
        try:                                                                                                     # Creates a scope to handle errors
            metrics = self.system.get_financial_metrics()                                                        # Retrieve financial metrics
        except Exception as err:                                                                                 # If any error is found, this block is executed
            print("Error obtaining financial metrics\n", err)                                                    # Prints error message

        if not metrics:                                                                                          # If no metrics are available, display an empty message
            print(METRICS.EMPTY_MESSAGE)                                                                # Displays empty text and positions it in the Frame
            on_switch_interface(0)
            
            return                                                                                               # Further code execution is stopped

        for idx, h in enumerate(METRICS.HEADERS):                                                                # Prepares to iterate over a list with the info subtitles, giving out its index and inner value
            print(h, round(metrics[idx], 2))                                                                     # Displays text with the header and positions it in the Frame

        is_valid = lambda num: num < 1 or num > 3
        message = """Please choose a valid operation:
                1) Make Query
                2) Download Full Report
                3) Return to main menu
                """
                
        action_number = input_loop(is_valid, message)

        if action_number == 1:
            self.submit_query()
        elif action_number == 2:
            self.generate_full_report()
        
        on_switch_interface(0)

    def submit_query(self):
        """Open a modal window to query specific data from the database.
        
        The modal allows users to:
        - Input queries in 'table:column' format
        - View query results in a scrollable listbox
        - Handle invalid queries with error messages
        """

        print("Input Query")                                                                        # Sets a text in the new frame and positions it
        print("Use '<table_name>:<column_name>' format\n(e.g. vehicles:id)")                        # Sets a text in the new frame and positions it
        query_entry = input()                                                                       # Creates an Entry component to receive user input
        query_list = query_entry.strip().split(':')                                           # Retrieves user input from Entry, deletes trailing spaces and splits it into a list of strings (separated by ':')

        if len(query_list) != 2:                                                                    # Condition to check if the input follows the format
            print("Please, enter a correct 'table' and a 'column'")                                 # Displays modal with error message
            return                                                                                  # Stops further code execution

        table_name, column_name = query_list                                                        # Extract table_name and column_name

        if table_name not in ["vehicles", "bookings", "logs"]:                                      # Validate the table name
            print("Please, enter a valid 'table'")                                                  # Shows error modal in case not an actual table 
            return                                                                                  # Stops further code execution

        try:                                                                                        # Creates a scope for error handling
            results_list = self.system.get_table_column(table_name, column_name)                    # Extracts database info with specified params
        except Exception:                                                                           # Handle invalid queries
            print(f"Please, enter a valid 'column' for table {table_name}")               # Displays error modal
            return                                                                                  # Stops further code execution

        if not results_list:                                                                        # Handle no results
            print("No results found.")     # Displays text when no data is found
            return

        print(f"{len(results_list)} results found:")  # Displays and positions the number of results found


        for item in results_list:                                                                   # Iterate over the list with the query results
            print(item[0])                                                         # Extract the results from their tuples and add them to the listbox

        print('\n')

    def generate_full_report(self):
        """Generate a comprehensive PDF report containing:
        - Vehicle inventory
        - Booking records
        - Transaction logs
        
        The report includes:
        - Timestamp in filename
        - Automatic pagination
        - Dynamic column sizing
        - Clear section headers
        """
        all_vehicles = self.system.get_all_vehicles()                                   # Retrieve a list with all vehicles from database
        all_bookings = self.system.get_all_bookings()                                   # Retrieve all bookings from database
        all_logs = self.system.get_all_logs()                                           # Retrieve all logs from database

        current_datetime = datetime.now()                                               # Get an object with the current date and time

        directory = f"{os.getcwd()}\\reports"
        os.makedirs(directory, exist_ok=True)
        filename = f"FullReport_{current_datetime.strftime('%Y-%m-%d_%H%M%S')}.pdf"
        file_path = f"{directory}\\{filename}"                                      # Opens a modal prompt for the user to choose a file path for the report

        if not file_path:                                                               # Exit if the user cancels the file dialog
            return                                                                      # Stops further code execution

        pdf = canvas.Canvas(file_path, pagesize=A4)                                     # Create a PDF file object to manipulate
        _, height = A4                                                                  # Obtain a variable with the PDF format's height
        y_position = height - 40                                                        # Start position for content

        pdf.setFont("Helvetica-Bold", 16)                                                                   # Set top text's font
        pdf.drawString(200, y_position, f"Full Report - {current_datetime.strftime('%Y-%m-%d_%H:%M:%S')}")  # Write the title's string on top of the file

        x_position = 50                                                                              # Adjust horizontal position
        y_position = height - 50                                                                     # Adjust vertical position for further text strings
        font_size = 8                                                                                # Define text size
        pdf.setFont("Helvetica", font_size)                                                          # Define text font and size for PDF object

        def draw_table(title, headers, data):
            """Draw a formatted table in the PDF document.
            
            Args:
                headers (list): Column headers for the table
                data (list): List of rows to display in the table
                
            Handles:
                - Dynamic column widths based on content
                - Automatic page breaks
                - Consistent formatting
            """
            nonlocal y_position                                                                           # Since variable 'y_position' is set outside of this scope, we need to remind the function to use its outter value
            x_pos = x_position                                                                            # TODO: Improve this -- we create a new variable with the same value, but can lead to errors
            
            pdf.drawString(x_position, y_position, title)                                               # Writes text to PDF with the displayed table's name
            y_position -= font_size * 1.5
            
            col_widths = [w * 5 + 10 for w in [max(len(str(item)) for item in col) for col in zip(headers, *data)]]     # Gets the max width for each column by finding the longest string length in headers and data and changes the scale of each width dynamically and returns the results
            pdf.setFont("Helvetica-Bold", font_size)                                                      # Set the font and size to be used in the PDF object
            
            for i, header in enumerate(headers):                                                          # Takes the index and inner value of the 'headers' list
                pdf.drawString(x_pos, y_position, header)                                                 # Writes the column names (headers) at the indicated position of the PDF
                x_pos += col_widths[i]                                                                    # Depending on the amount of columns, the horizontal position is moved
            
            y_position -= font_size * 1.25                                                                # Lowers the vertical position of the pointer, in accordance to the row's text size
            pdf.setFont("Helvetica", font_size)                                                           # Set the rows' font and size

            for row in data:                                                                              # Iterate over the list of database content
                x_pos = x_position                                                                        # TODO: Improve this -- we create a new variable with the same value, but can lead to errors
                for i, cell in enumerate(row):                                                            # Extract each piece of information from the row's list and their index
                    pdf.drawString(x_pos, y_position, str(cell))                                          # Writes the information to the PDF, aligned with its corresponding column
                    x_pos += col_widths[i]                                                                # Moves the PDF object's pointer to the next column's horizontal position
                y_position -= font_size * 1.25                                                            # Move the vertical pointer to the next row's position, in accordance to the row's text size
                if y_position < 50:                                                                       # Checks if vertical position is close to the end of the page
                    pdf.showPage()                                                                        # Closes current page and if needed, starts a new one
                    y_position = height - 50                                                              # Resets the vertical pointer at the top of the page's size
            
            y_position -= font_size * 2.5

        draw_table("Vehicles:", METRICS.PDF_HEADERS.VEHICLES, all_vehicles)                                            # Uses table information to generate, format, and print the PDF's contents
        draw_table("Bookings:", METRICS.PDF_HEADERS.BOOKINGS, all_bookings)                                            # Uses table information to generate, format, and print the PDF's contents
        draw_table("Transaction Logs:", METRICS.PDF_HEADERS.LOGS, all_logs)                                            # Uses table information to generate, format, and print the PDF's contents

        pdf.save()                                                                                        # Generate the final PDF file in the previously accorded path
        print(f"Report saved as {file_path}\n\n")                                                             # Show a success message on the developer's console with the new file's path