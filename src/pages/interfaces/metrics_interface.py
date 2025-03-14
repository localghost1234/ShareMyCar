import tkinter as tk
from tkinter import filedialog
from src.pages.interfaces.base_interface import BaseInterface
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from src.misc.strings import METRICS

class MetricsInterface(BaseInterface):
    """Interface for displaying financial metrics and generating reports.

    This class provides functionality to view financial metrics, query specific data,
    and generate a full report in PDF format.
    """

    def __init__(self, root, system):
        """Initialize the MetricsInterface.

        Args:
            root: The root Tkinter window.
            system: The core system instance.
        """
        super().__init__(root, system, *METRICS.TITLES)  # Initialize the base interface with titles

        metrics = self.system.get_financial_metrics()  # Retrieve financial metrics

        if not metrics:  # If no metrics are available, display an empty message
            tk.Label(self.frame, text=METRICS.EMPTY_MESSAGE, font=("Arial", 18, "bold")).pack(padx=50, pady=50)
            return

        for idx, h in enumerate(METRICS.HEADERS):  # Display each metric with its header
            tk.Label(self.frame, text=h, font=("Arial", 13, "bold")).pack(pady=5)
            tk.Label(self.frame, text=round(metrics[idx], 2), font=("Arial", 12, "italic")).pack()

        tk.Button(self.frame, text="Make Query", command=self.show_querying_modal).pack(pady=20)  # Query button
        tk.Button(self.frame, text="Download Full Report", command=self.generate_full_report).pack()  # Report button

    def show_querying_modal(self):
        """Open a modal window to query specific data from the database."""
        modal_window = tk.Toplevel(self.frame)  # Create a modal window
        modal_window.title("Query Data")
        modal_window.geometry("360x400")

        tk.Label(modal_window, text="Input Query", font=("Arial", 16, "bold")).pack(pady=7)
        tk.Label(modal_window, text="Use 'key:value' format\n(e.g. vehicles:id, bookings:custome_name, logs:vehicle_id)", font=("Arial", 9, "italic")).pack()

        query_entry = tk.Entry(modal_window, font=("Arial", 10))  # Entry field for query
        query_entry.pack(pady=10)

        def submit_query():
            """Submit the query and display results in the modal window."""
            query_list = query_entry.get().strip().split(':')  # Split the query into key and value

            if len(query_list) != 2:  # Validate the query format
                self.show_error("Please, enter a 'key' and a 'value' only")
                return

            key, value = query_list  # Extract key and value

            if key not in ["vehicles", "bookings", "logs"]:  # Validate the table name
                self.show_error("Please, enter a valid table name")
                return

            try:  # Execute the query
                results_list = self.system.database.execute_query(
                    operation="SELECT",
                    table=key,
                    columns=[value],
                    fetch="all"
                )
            except Exception:  # Handle invalid queries
                self.show_error(f"Please, enter a valid value for table {key}")
                return

            # Clear existing widgets in the modal window
            for widget in modal_window.winfo_children():
                if isinstance(widget, tk.Listbox):
                    widget.destroy()  # Destroy the existing Listbox
                elif isinstance(widget, tk.Label) and widget.cget("text").startswith(f"{len(results_list)} results found:"):
                    widget.destroy()
                elif isinstance(widget, tk.Label) and widget.cget("text").startswith("No result found."):
                    widget.destroy()
                elif isinstance(widget, tk.Scrollbar):
                    widget.destroy()

            if not results_list:  # Handle no results
                tk.Label(modal_window, text="No results found.", font=("Arial", 12)).pack(pady=15)
                return

            # Display the number of results found
            tk.Label(modal_window, text=f"{len(results_list)} results found:", font=("Arial", 12)).pack(pady=15)

            # Add a scrollable listbox to display results
            v_scrollbar = tk.Scrollbar(modal_window, orient=tk.VERTICAL)
            listbox = tk.Listbox(modal_window, yscrollcommand=v_scrollbar.set, font=("Arial", 10))
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.pack(fill=tk.Y)
            v_scrollbar.config(command=listbox.yview)

            for item in results_list:  # Populate the listbox with results
                listbox.insert(tk.END, item[0])

        tk.Button(modal_window, text="Search", command=submit_query).pack()  # Query submission button

    def generate_full_report(self):
        """Generate a full report in PDF format containing vehicles, bookings, and logs."""
        all_vehicles = self.system.get_all_vehicles()  # Retrieve all vehicles
        all_bookings = self.system.get_all_bookings()  # Retrieve all bookings
        all_logs = self.system.get_transaction_logs()  # Retrieve all logs

        current_datetime = datetime.now()  # Get the current date and time

        # Prompt the user to choose a file path for the report
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Choose Report Folder",
            initialfile=f"FullReport_{current_datetime.strftime('%Y-%m-%d_%H%M%S')}"
        )

        if not file_path:  # Exit if the user cancels the file dialog
            return

        pdf = canvas.Canvas(file_path, pagesize=A4) # Create a PDF canvas
        _, height = A4 # Obtain a variable with the PDF format's height
        y_position = height - 40  # Start position for content

        # Add the report title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, y_position, f"Full Report - {current_datetime.strftime('%Y-%m-%d_%H:%M:%S')}")
        y_position -= 30

        x_position = 50  # Start x position for content
        y_position = height - 50
        font_size = 8
        pdf.setFont("Helvetica", font_size)

        def compute_column_widths(headers, data):
            """Compute column widths based on the longest item in each column.

            Args:
                headers: The column headers.
                data: The data to be displayed.

            Returns:
                list: A list of column widths.
            """
            col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]
            return [w * 5 + 10 for w in col_widths]  # Scale widths dynamically

        def draw_table(headers, data, col_widths):
            """Draw a table in the PDF.

            Args:
                headers: The column headers.
                data: The data to be displayed.
                col_widths: The computed column widths.
            """
            nonlocal y_position
            x_pos = x_position
            pdf.setFont("Helvetica-Bold", font_size)
            for i, header in enumerate(headers):  # Draw headers
                pdf.drawString(x_pos, y_position, header)
                x_pos += col_widths[i]
            y_position -= 10
            pdf.setFont("Helvetica", font_size)

            for row in data:  # Draw rows
                x_pos = x_position
                for i, cell in enumerate(row):
                    pdf.drawString(x_pos, y_position, str(cell))
                    x_pos += col_widths[i]
                y_position -= 10
                if y_position < 50:  # Start a new page if the current page is full
                    pdf.showPage()
                    pdf.setFont("Helvetica", font_size)
                    y_position = height - 50

        # Compute column widths for each table
        vehicle_col_widths = compute_column_widths(METRICS.PDF_HEADERS.VEHICLES, all_vehicles)
        booking_col_widths = compute_column_widths(METRICS.PDF_HEADERS.BOOKINGS, all_bookings)
        log_col_widths = compute_column_widths(METRICS.PDF_HEADERS.LOGS, all_logs)

        # Add vehicles data to the PDF
        pdf.drawString(x_position, y_position, "Vehicles:")
        y_position -= 15
        draw_table(METRICS.PDF_HEADERS.VEHICLES, all_vehicles, vehicle_col_widths)
        y_position -= 20

        # Add bookings data to the PDF
        pdf.drawString(x_position, y_position, "Bookings:")
        y_position -= 15
        draw_table(METRICS.PDF_HEADERS.BOOKINGS, all_bookings, booking_col_widths)
        y_position -= 20

        # Add transaction logs to the PDF
        pdf.drawString(x_position, y_position, "Transaction Logs:")
        y_position -= 15
        draw_table(METRICS.PDF_HEADERS.LOGS, all_logs, log_col_widths)

        pdf.save()  # Save the PDF
        print(f"Report saved as {file_path}")