from tkinter import Label, Button, filedialog
from src.pages.interfaces.base_interface import BaseInterface
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

titles = ("Metrics Management", "Financial Metrics")
headers = ("Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)")
empty_message = "No financial data available."

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        self.metrics = self.system.get_financial_metrics()

        Label(self.frame, text="Total Revenue (€):", font=("Arial", 10, "bold")).pack(pady=5)
        Label(self.frame, text=self.metrics[0], font=("Arial", 8, "italic")).pack()

        Label(self.frame, text="Total Operational Costs (€):", font=("Arial", 10, "bold")).pack(pady=5)
        Label(self.frame, text=self.metrics[1], font=("Arial", 8, "italic")).pack()

        Label(self.frame, text="Total Profit (€):", font=("Arial", 10, "bold")).pack(pady=5)
        Label(self.frame, text=self.metrics[2], font=("Arial", 8, "italic")).pack()

        Label(self.frame, text="Average Mileage Per Vehicle (km):", font=("Arial", 10, "bold")).pack(pady=5)
        Label(self.frame, text=self.metrics[3], font=("Arial", 8, "italic")).pack()

        Button(self.frame, text="Query Metric", command=self.query_metric).pack(pady=20)
        Button(self.frame, text="Download Full Report", command=self.generate_full_report).pack(pady=2)

    def query_metric(self):
        pass

    def generate_full_report(self):
        all_vehicles = self.system.get_all_vehicles()
        all_bookings = self.system.get_all_bookings()
        all_logs = self.system.get_transaction_logs()

        file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Report As"
    )

        if not file_path:  # User cancelled
            return

        # Create PDF
        pdf = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y_position = height - 40  # Start position

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(200, y_position, "Full System Report")
        y_position -= 30

        pdf.setFont("Helvetica", 12)

        # **1. Add Vehicles Data**
        pdf.drawString(50, y_position, "Vehicles:")
        y_position -= 20

        for vehicle in all_vehicles:
            pdf.drawString(50, y_position, f"ID: {vehicle[0]}, Brand: {vehicle[1]}, Model: {vehicle[2]}")
            y_position -= 15
            if y_position < 50:  # New page if needed
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = height - 40

        # **2. Add Booking Data**
        pdf.drawString(50, y_position, "Bookings:")
        y_position -= 20

        for booking in all_bookings:
            pdf.drawString(50, y_position, f"Booking ID: {booking[0]}, Vehicle ID: {booking[1]}, User: {booking[2]}")
            y_position -= 15
            if y_position < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = height - 40

        # **3. Add Transaction Logs**
        pdf.drawString(50, y_position, "Transaction Logs:")
        y_position -= 20

        for log in all_logs:
            pdf.drawString(50, y_position, f"Log ID: {log[0]}, Amount: {log[1]}€, Date: {log[2]}")
            y_position -= 15
            if y_position < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = height - 40

        # Save the PDF
        pdf.save()
        print(f"Report saved as {file_path}")
