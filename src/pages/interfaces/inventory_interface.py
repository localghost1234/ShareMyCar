import tkinter as tk
from tkinter import messagebox
from src.pages.interfaces.base_interface import BaseInterface

class InventoryInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Inventory Management", system)

        tk.Label(self.frame, text="Vehicle Inventory:").pack()

        # Frame for vehicle list with scrollbars
        self.vehicle_frame = tk.Frame(self.frame)
        self.vehicle_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        self.v_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.VERTICAL)
        self.h_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.HORIZONTAL)

        # Listbox to display vehicles
        self.vehicle_listbox = tk.Listbox(
            self.vehicle_frame, height=15, width=100,
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set,
            font=("Courier", 10)  # Use a monospaced font for alignment
        )

        # Pack elements properly
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vehicle_listbox.pack(fill=tk.BOTH, expand=True)

        # Link scrollbar
        self.v_scrollbar.config(command=self.vehicle_listbox.yview)

        # Load vehicles
        self.load_vehicles()

        # Add button for adding a new vehicle
        self.add_button = tk.Button(self.frame, text="Add Vehicle", command=self.add_vehicle)
        self.add_button.pack(padx=10, pady=10)

    def load_vehicles(self):
        """Fetches and displays all vehicles in the inventory."""
        self.vehicle_listbox.delete(0, tk.END)  # Clear the listbox

        vehicles = self.system.get_all_vehicles()  # Add this method to your system class
        
        if vehicles:
            # Define column headers
            headers = ["ID", "Brand", "Model", "Mileage (kms)", "Daily Price", "Maintenance Cost", "Available"]
            header_row = (
                f"{headers[0]:<5} | "
                f"{headers[1]:<15} | "
                f"{headers[2]:<15} | "
                f"{headers[3]:<15} | "
                f"{headers[4]:<10} | "
                f"{headers[5]:<15} | "
                f"{headers[6]:<10}"
            )
            self.vehicle_listbox.insert(tk.END, header_row)  # Insert headers
            self.vehicle_listbox.insert(tk.END, "-" * 120)  # Insert a separator line

            for v in vehicles:
                vehicle_info = (
                    f"{v[0]:<5} | "
                    f"{v[1]:<15} | "
                    f"{v[2]:<15} | "
                    f"{v[3]:<15} | "
                    f"€{v[4]:<9} | "
                    f"€{v[5]:<14} | "
                    f"{'Yes' if v[6] else 'No':<10}"
                )
                self.vehicle_listbox.insert(tk.END, vehicle_info)
        else:
            self.vehicle_listbox.insert(tk.END, "No vehicles available.")

    def add_vehicle(self):
        """Handles adding a new vehicle to the system."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Vehicle")
        dialog.geometry("300x200")

        tk.Label(dialog, text="Brand:").grid(row=0, column=0, padx=10, pady=5)
        brand_entry = tk.Entry(dialog)
        brand_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Model:").grid(row=1, column=0, padx=10, pady=5)
        model_entry = tk.Entry(dialog)
        model_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Mileage:").grid(row=2, column=0, padx=10, pady=5)
        mileage_entry = tk.Entry(dialog)
        mileage_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Daily Price:").grid(row=3, column=0, padx=10, pady=5)
        daily_price_entry = tk.Entry(dialog)
        daily_price_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Maintenance Cost:").grid(row=4, column=0, padx=10, pady=5)
        maintenance_cost_entry = tk.Entry(dialog)
        maintenance_cost_entry.grid(row=4, column=1, padx=10, pady=5)

        submit_button = tk.Button(dialog, text="Submit", command=lambda: self.submit_vehicle(
            brand_entry.get(),
            model_entry.get(),
            mileage_entry.get(),
            daily_price_entry.get(),
            maintenance_cost_entry.get(),
            dialog
        ))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_vehicle(self, brand, model, mileage, daily_price, maintenance_cost, dialog):
        """Validates and submits a new vehicle entry."""
        if not brand or not model or not mileage or not daily_price or not maintenance_cost:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            mileage = int(mileage)
            daily_price = float(daily_price)
            maintenance_cost = float(maintenance_cost)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for mileage, daily price, or maintenance cost.")
            return

        self.system.add_vehicle(brand, model, mileage, daily_price, maintenance_cost)
        messagebox.showinfo("Success", "Vehicle added!")

        dialog.destroy()
        self.load_vehicles()  # Reload vehicles after adding