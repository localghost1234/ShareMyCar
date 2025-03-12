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
booking_headers = ("ID", "Vehicle ID", "Rental Days", "Estimated KM", "Estimated Cost", "Start Date", "End Date", "Customer Name")
log_headers = ("ID", "Vehicle ID", "Rental Duration", "Revenue", "Additional Costs", "Customer Name")

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        self.metrics = self.system.get_financial_metrics()

        new_frame = tk.Frame(self.frame)

        tk.Button(new_frame, text="Download Full Report", command=self.generate_full_report).grid(row=0, column=0, pady=2)

        tk.Label(new_frame, text="Total Revenue (€):", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=5)
        tk.Label(new_frame, text=self.metrics[0], font=("Arial", 8, "italic")).grid(row=1, column=1)

        tk.Label(new_frame, text="Total Operational Costs (€):", font=("Arial", 10, "bold")).grid(row=2, column=0, pady=5)
        tk.Label(new_frame, text=self.metrics[1], font=("Arial", 8, "italic")).grid(row=2, column=1)

        tk.Label(new_frame, text="Total Profit (€):", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=5)
        tk.Label(new_frame, text=self.metrics[2], font=("Arial", 8, "italic")).grid(row=3, column=1)

        tk.Label(new_frame, text="Average Mileage Per Vehicle (km):", font=("Arial", 10, "bold")).grid(row=4, column=0, pady=5)
        tk.Label(new_frame, text=self.metrics[3], font=("Arial", 8, "italic")).grid(row=4, column=1)

        query_var = tk.StringVar()
        tk.Label(new_frame, text="Enter query in a 'key:value' format (e.g. vehicle:id, booking:start_date)", font=("Arial", 10, "bold")).grid(row=5, column=0, pady=5)
        tk.Entry(new_frame, textvariable=query_var).grid(row=6, column=0)

        # tk.Button to execute the query
        tk.Button(new_frame, text="Display Query", command=lambda: self.system.database.execute_query(query_var.get())).grid(row=7, pady=15)

        tk.Label(new_frame, text="No results found!", font=("Arial", 12)).grid(row=8, padx=15, pady=15)

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
        pdf.drawString(200, y_position, f"Full Car Sharing Report - {current_datetime.strftime("%Y-%m-%d_%H:%M:%S")}")
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
