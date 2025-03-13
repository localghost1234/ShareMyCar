import tkinter as tk
from tkinter import filedialog
from src.pages.interfaces.base_interface import BaseInterface
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

titles = ("Metrics Management", "Financial Metrics")
headers = ("Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)")
empty_message = "No financial data available."

vehicle_headers = ("ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost", "Available", "Maintenance Mileage")
booking_headers = ("ID", "Vehicle ID", "Rental Days", "Estimated KM", "Estimated Cost", "Customer Name")
log_headers = ("ID", "Vehicle ID", "Rental Duration", "Revenue", "Additional Costs", "Customer Name", "Transaction Type")

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        metrics = self.system.get_financial_metrics()

        if not metrics:
            tk.Label(self.frame, text=empty_message, font=("Arial", 18, "bold")).pack(padx=50, pady=50)
            return

        for idx, h in enumerate(headers):
            tk.Label(self.frame, text=h, font=("Arial", 13, "bold")).pack(pady=5)
            tk.Label(self.frame, text=metrics[0], font=("Arial", 12, "italic")).pack()

        tk.Button(self.frame, text="Query Metric", command=self.query_metric).pack(pady=20)
        tk.Button(self.frame, text="Download Full Report", command=self.generate_full_report).pack()

    def query_metric(self):
        """Open a modal window to query specific data."""
        # Create a modal window
        modal_window = tk.Toplevel(self.frame)
        modal_window.title("Query Data")
        modal_window.geometry("360x400")
        
        tk.Label(modal_window, text="Input Query", font=("Arial", 16, "bold")).pack(pady=7)
        tk.Label(modal_window, text="Use 'key:value' format\n(e.g. vehicle:id, booking:custome_name, log:vehicle_id)", font=("Arial", 11, "italic")).pack()
        
        query_entry = tk.Entry(modal_window, font=("Arial", 10))
        query_entry.pack(pady=10)

        def submit_query():            
            nonlocal modal_window
            nonlocal query_entry

            query_list = query_entry.get().strip().split(':')
            
            if len(query_list) != 2:
                self.show_error("Please, enter a 'key' and a 'value' only")
                return
            
            key = query_list[0]
            value = query_list[1]

            query_statement = f"SELECT {value} FROM {key}s"
            self.system.database.execute_query(query_statement)
            result_list = self.system.database.cursor.fetchall()

            for widget in modal_window.winfo_children():                
                if isinstance(widget, tk.Listbox):
                    widget.destroy()  # Destroy the existing Listbox
                elif isinstance(widget, tk.Label) and widget.cget("text").startswith(f"{len(result_list)} results found:"):
                    widget.destroy()
                elif isinstance(widget, tk.Label) and widget.cget("text").startswith("No result found."):
                    widget.destroy()
                elif isinstance(widget, tk.Scrollbar):
                    widget.destroy()
            
            if not len(result_list):
                tk.Label(modal_window, text="No results found.", font=("Arial", 12)).pack(pady=15)
                return
            
            tk.Label(modal_window, text=f"{len(result_list)} results found:", font=("Arial", 12)).pack(pady=15)
            
            v_scrollbar = tk.Scrollbar(modal_window, orient=tk.VERTICAL)

            listbox = tk.Listbox(
                modal_window,
                yscrollcommand=v_scrollbar.set,
                font=("Arial", 10)
            )

            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.pack(fill=tk.Y)

            # Link scrollbars
            v_scrollbar.config(command=listbox.yview)

            for item in result_list:
                listbox.insert(tk.END, item[0])

        # tk.Button to execute the query
        tk.Button(modal_window, text="Search", command=submit_query).pack()

    def generate_full_report(self):
        all_vehicles = self.system.get_all_vehicles()
        all_bookings = self.system.get_all_bookings()
        all_logs = self.system.get_transaction_logs()

        current_datetime = datetime.now()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Choose Report Folder",
            initialfile=f"FullReport_{current_datetime.strftime("%Y-%m-%d_%H%M%S")}"
        )

        if not file_path:  # User cancelled
            return

        # Create PDF
        pdf = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y_position = height - 40  # Start position

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, y_position, f"Full Report - {current_datetime.strftime("%Y-%m-%d_%H:%M:%S")}")
        y_position -= 30

        x_position = 50
        y_position = height - 50
        font_size = 8
        pdf.setFont("Helvetica", font_size)

        # Compute column widths based on the longest item in each column
        def compute_column_widths(headers, data):
            col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]
            return [w * 5 + 10 for w in col_widths]  # Scale widths dynamically

        # Helper function to calculate max column widths
        def draw_table(headers, data, col_widths):
            nonlocal y_position
            x_pos = x_position
            pdf.setFont("Helvetica-Bold", font_size)
            for i, header in enumerate(headers):
                pdf.drawString(x_pos, y_position, header)
                x_pos += col_widths[i]
            y_position -= 10
            pdf.setFont("Helvetica", font_size)
            
            for row in data:
                x_pos = x_position
                for i, cell in enumerate(row):
                    pdf.drawString(x_pos, y_position, str(cell))
                    x_pos += col_widths[i]
                y_position -= 10
                if y_position < 50:
                    pdf.showPage()
                    pdf.setFont("Helvetica", font_size)
                    y_position = height - 50

        vehicle_col_widths = compute_column_widths(vehicle_headers, all_vehicles)
        booking_col_widths = compute_column_widths(booking_headers, all_bookings)
        log_col_widths = compute_column_widths(log_headers, all_logs)

        # **1. Add Vehicles Data**
        pdf.drawString(x_position, y_position, "Vehicles:")
        y_position -= 15
        draw_table(vehicle_headers, all_vehicles, vehicle_col_widths)
        y_position -= 20

        # **2. Add Booking Data**
        pdf.drawString(x_position, y_position, "Bookings:")
        y_position -= 15
        draw_table(booking_headers, all_bookings, booking_col_widths)
        y_position -= 20

        # **3. Add Transaction Logs**
        pdf.drawString(x_position, y_position, "Transaction Logs:")
        y_position -= 15
        draw_table(log_headers, all_logs, log_col_widths)

        pdf.save()
        print(f"Report saved as {file_path}")
