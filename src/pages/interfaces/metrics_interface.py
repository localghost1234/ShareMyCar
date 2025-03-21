import tkinter as tk                                            # Import the tkinter library for creating the GUI, aliased as 'tk' for convenience
from tkinter import filedialog                                  # Import the filedialog module from tkinter for opening and saving file dialogs
from src.pages.interfaces.base_interface import BaseInterface   # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from reportlab.lib.pagesizes import A4                          # Import the A4 constant from reportlab, defining the standard A4 page size for PDF generation
from reportlab.pdfgen import canvas                             # Import the canvas class from reportlab for creating and drawing on PDF documents
from datetime import datetime                                   # Import the datetime class for working with dates and times
from src.misc.strings import METRICS                            # Import the METRICS constant, containing strings or configurations for the metrics interface

class MetricsInterface(BaseInterface):
    """Interface for displaying financial metrics and generating reports.

        This class provides functionality to view financial metrics, query specific data,
        and generate a full report in PDF format.
    """

    def __init__(self, root, system):
        super().__init__(root, system, *METRICS.TITLES)                                                          # Initializes 'BaseInterface' with the pre-defined TITLES strings

        metrics = ()                                                                                             # Initializes tuple with the metrics info
        
        try:                                                                                                     # Creates a scope to handle errors
            metrics = self.system.get_financial_metrics()                                                        # Retrieve financial metrics
        except Exception as err:                                                                                 # If any error is found, this block is executed
            print("Error obtaining financial metrics\n", err)                                                    # Prints error message

        if not metrics:                                                                                          # If no metrics are available, display an empty message
            tk.Label(self.frame, text=METRICS.EMPTY_MESSAGE, font=("Arial", 18, "bold")).pack(padx=50, pady=50)  # Displays empty text and positions it in the Frame
            return                                                                                               # Further code execution is stopped

        for idx, h in enumerate(METRICS.HEADERS):                                                                # Prepares to iterate over a list with the info subtitles, giving out its index and inner value
            tk.Label(self.frame, text=h, font=("Arial", 13, "bold")).pack(pady=5)                                # Displays text with the header and positions it in the Frame
            tk.Label(self.frame, text=round(metrics[idx], 2), font=("Arial", 12, "italic")).pack()               # Displays text with the data collected from the database

        tk.Button(self.frame, text="Make Query", command=self.show_querying_modal).pack(pady=20)                 # Sets a button which opens the querying making modal
        tk.Button(self.frame, text="Download Full Report", command=self.generate_full_report).pack()             # Sets a button which opens allows saving a PDF with a report

    def show_querying_modal(self):
        """Open a modal window to query specific data from the database."""
        modal_window = tk.Toplevel(self.frame)                                                                                               # Creates a modal component and links it to the main Frame
        modal_window.title("Query Data")                                                                                                     # Puts a title on the modal
        modal_window.geometry("360x400")                                                                                                     # Sets modal's size

        instructions_frame = tk.Frame(modal_window)                                                                                          # Creates a new Frame inside the modal window
        instructions_frame.pack(fill=tk.BOTH)                                                                                                # Positions the frame and expands it to fill the modal

        tk.Label(instructions_frame, text="Input Query", font=("Arial", 16, "bold")).pack(pady=7)                                            # Sets a text in the new frame and positions it
        tk.Label(instructions_frame, text="Use '<table_name>:<column_name>' format\n(e.g. vehicles:id)", font=("Arial", 9, "italic")).pack() # Sets a text in the new frame and positions it

        query_entry = tk.Entry(instructions_frame, font=("Arial", 10))                                                                       # Creates an Entry component to receive user input
        query_entry.pack(pady=10)                                                                                                            # Positions the Entry component

        listbox_frame = tk.Frame(modal_window)                                                                                               # Creates a new Frame linked to the modal window, where the query results will be set
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=15)                                                                               # Positions the frame and makes it expand around the modal, below the 'instructions_frame'

        def submit_query():
            """Submit the query and display results in the modal window."""
            query_list = query_entry.get().strip().split(':')                                           # Retrieves user input from Entry, deletes trailing spaces and splits it into a list of strings (separated by ':')

            if len(query_list) != 2:                                                                    # Condition to check if the input follows the format
                self.show_error("Please, enter a correct 'table' and a 'column'")                       # Displays modal with error message
                return                                                                                  # Stops further code execution

            table_name, column_name = query_list                                                        # Extract table_name and column_name

            if table_name not in ["vehicles", "bookings", "logs"]:                                      # Validate the table name
                self.show_error("Please, enter a valid 'table'")                                        # Shows error modal in case not an actual table 
                return                                                                                  # Stops further code execution

            try:                                                                                        # Creates a scope for error handling
                results_list = self.system.get_table_column(table_name, column_name)                    # Extracts database info with specified params
            except Exception:                                                                           # Handle invalid queries
                self.show_error(f"Please, enter a valid 'column' for table {table_name}")               # Displays error modal
                return                                                                                  # Stops further code execution

            for widget in listbox_frame.winfo_children():                                               # Iterates over all components in the listbox Frame
                widget.destroy()                                                                        # Deletes the component

            if not results_list:                                                                        # Handle no results
                tk.Label(listbox_frame, text="No results found.", font=("Arial", 12)).pack(pady=15)     # Displays text when no data is found
                return

            tk.Label(listbox_frame, text=f"{len(results_list)} results found:", font=("Arial", 12)).pack(pady=15)   # Displays and positions the number of results found

            v_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)                               # Create a Scrollbar component to move vertically around the Listbox
            listbox = tk.Listbox(listbox_frame, yscrollcommand=v_scrollbar.set, font=("Arial", 10))     # Listbox object is created, stylized, and linked to Scrollbar
            v_scrollbar.config(command=listbox.yview)                                                   # Scrollbar is linked to Listbox
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)                                                  # Scrollbar is positioned in the Frame
            listbox.pack(fill=tk.Y)                                                                     # Listbox is positioned in the Frame

            for item in results_list:                                                                   # Iterate over the list with the query results
                listbox.insert(tk.END, item[0])                                                         # Extract the results from their tuples and add them to the listbox

        tk.Button(instructions_frame, text="Search", command=submit_query).pack()                       # Creates Button component and links it to submission function

    def generate_full_report(self):
        """Generate a full report in PDF format containing vehicles, bookings, and logs."""
        all_vehicles = self.system.get_all_vehicles()                                   # Retrieve a list with all vehicles from database
        all_bookings = self.system.get_all_bookings()                                   # Retrieve all bookings from database
        all_logs = self.system.get_all_logs()                                           # Retrieve all logs from database

        current_datetime = datetime.now()                                               # Get an object with the current date and time

        file_path = filedialog.asksaveasfilename(                                       # Opens a modal prompt for the user to choose a file path for the report
            defaultextension=".pdf",                                                    # Appends extension to filename if none is given
            filetypes=[("PDF Files", "*.pdf")],                                         # Filters all searches and saves to allow only PDF
            title="Choose Report Folder",                                               # The title that appears at the top of the modal
            initialfile=f"FullReport_{current_datetime.strftime('%Y-%m-%d_%H%M%S')}",   # Default filename with determined date and time format
        )

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

        def draw_table(headers, data):
            """Draw a table in the PDF.

            Args:
                headers: The column headers.
                data: The data to be displayed.
                col_widths: The computed column widths.
            """
            col_widths = [w * 5 + 10 for w in [max(len(str(item)) for item in col) for col in zip(headers, *data)]]     # Gets the max width for each column by finding the longest string length in headers and data and changes the scale of each width dynamically and returns the results
            
            nonlocal y_position                                                                           # Since variable 'y_position' is set outside of this scope, we need to remind the function to use its outter value
            x_pos = x_position                                                                            # TODO: Improve this -- we create a new variable with the same value, but can lead to errors
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

        pdf.drawString(x_position, y_position, "Vehicles:")                                               # Writes text to PDF with the displayed table's name
        y_position -= font_size * 1.5                                                                     # Moves vertical pointer down according to the text's size
        draw_table(METRICS.PDF_HEADERS.VEHICLES, all_vehicles)                                            # Uses table information to generate, format, and print the PDF's contents
        y_position -= font_size * 2.5                                                                     # Moves vertical pointer down according to the text's size

        pdf.drawString(x_position, y_position, "Bookings:")                                               # Writes text to PDF with the displayed table's name
        y_position -= font_size * 1.5                                                                     # Moves vertical pointer down according to the text's size
        draw_table(METRICS.PDF_HEADERS.BOOKINGS, all_bookings)                                            # Uses table information to generate, format, and print the PDF's contents
        y_position -= font_size * 2.5                                                                     # Moves vertical pointer down according to the text's size

        pdf.drawString(x_position, y_position, "Transaction Logs:")                                       # Writes text to PDF with the displayed table's name
        y_position -= font_size * 1.5                                                                     # Moves vertical pointer down according to the text's size
        draw_table(METRICS.PDF_HEADERS.LOGS, all_logs)                                                    # Uses table information to generate, format, and print the PDF's contents

        pdf.save()                                                                                        # Generate the final PDF file in the previously accorded path
        print(f"Report saved as {file_path}")                                                             # Show a success message on the developer's console with the new file's path