# booking_interface.py
import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.strings import BOOKING

class BookingInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, BOOKING.TITLE)

        # Vehicle ID input
        tk.Label(self.frame, text="Vehicle ID:", font=("Arial", 12)).pack(pady=5)
        self.vehicle_id_entry = tk.Entry(self.frame)
        self.vehicle_id_entry.pack()

        # Customer Name input
        tk.Label(self.frame, text="Customer Name:", font=("Arial", 12)).pack(pady=5)
        self.customer_name_entry = tk.Entry(self.frame)
        self.customer_name_entry.pack()

        # Rental days input
        tk.Label(self.frame, text="Rental Duration (days):", font=("Arial", 12)).pack(pady=5)
        self.rental_days_entry = tk.Entry(self.frame)
        self.rental_days_entry.pack()

        # Estimated kilometers input
        tk.Label(self.frame, text="Estimated Kilometers:", font=("Arial", 12)).pack(pady=5)
        self.estimated_km_entry = tk.Entry(self.frame)
        self.estimated_km_entry.pack()

        # Book button
        self.book_button = tk.Button(self.frame, text="Book Vehicle", command=self.create_booking)
        self.book_button.pack(pady=25)

    def create_booking(self):
        """Handles booking process by taking input values and calling system logic."""
        try:
            vehicle_id = int(self.vehicle_id_entry.get())
            rental_days = int(self.rental_days_entry.get())
            estimated_km = int(self.estimated_km_entry.get())
            customer_name = str(self.customer_name_entry.get())

            cost = self.system.query_booking(vehicle_id, rental_days, estimated_km, customer_name)
            
            if cost:
                self.show_info(f"Vehicle booked! Estimated cost: €{cost}")
            else:
                self.show_error("Vehicle not found or unavailable.")
        except ValueError:
            self.show_error("Please enter valid values.")
