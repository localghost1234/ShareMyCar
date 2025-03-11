import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

headers = ("ID", "Brand", "Model", "Mileage (kms)", "Daily Price", "Maintenance Cost", "Available")
header_row = (
    f"{headers[0]:<5} | "
    f"{headers[1]:<15} | "
    f"{headers[2]:<15} | "
    f"{headers[3]:<15} | "
    f"{headers[4]:<10} | "
    f"{headers[5]:<15} | "
    f"{headers[6]:<10}"
)
separator_row = "-" * 120

class InventoryInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root,  system, "Inventory Management", "Vehicle Inventory")

        self.create_scrollable_listbox()

        self.add_button = tk.Button(self.frame, text="Add Vehicle", command=self.add_vehicle)
        self.add_button.pack(padx=10, pady=10)

    def load_vehicles(self):
        self.listbox.delete(0, tk.END)  # Clear the listbox

        vehicles = self.system.get_all_vehicles()  # Fetch vehicles
        
        if vehicles:
            self.listbox.insert(tk.END, header_row)  # Insert headers
            self.listbox.insert(tk.END, separator_row)  # Insert a separator line

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
                self.listbox.insert(tk.END, vehicle_info)
        else:
            self.listbox.insert(tk.END, "No vehicles available.")

    def add_vehicle(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Vehicle")
        dialog.geometry("300x200")

        # Brand input
        tk.Label(dialog, text="Brand:").grid(row=0, column=0, padx=10, pady=5)
        brand_entry = tk.Entry(dialog)
        brand_entry.grid(row=0, column=1, padx=10, pady=5)

        # Model input
        tk.Label(dialog, text="Model:").grid(row=1, column=0, padx=10, pady=5)
        model_entry = tk.Entry(dialog)
        model_entry.grid(row=1, column=1, padx=10, pady=5)

        # Mileage input
        tk.Label(dialog, text="Mileage:").grid(row=2, column=0, padx=10, pady=5)
        mileage_entry = tk.Entry(dialog)
        mileage_entry.grid(row=2, column=1, padx=10, pady=5)

        # Daily Price input
        tk.Label(dialog, text="Daily Price:").grid(row=3, column=0, padx=10, pady=5)
        daily_price_entry = tk.Entry(dialog)
        daily_price_entry.grid(row=3, column=1, padx=10, pady=5)

        # Maintenance Cost input
        tk.Label(dialog, text="Maintenance Cost:").grid(row=4, column=0, padx=10, pady=5)
        maintenance_cost_entry = tk.Entry(dialog)
        maintenance_cost_entry.grid(row=4, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(
            dialog, text="Submit",
            command=lambda: self.submit_vehicle(
                brand_entry.get(),
                model_entry.get(),
                mileage_entry.get(),
                daily_price_entry.get(),
                maintenance_cost_entry.get(),
                dialog
            )
        )
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_vehicle(self, brand, model, mileage, daily_price, maintenance_cost, dialog):
        if not brand or not model or not mileage or not daily_price or not maintenance_cost:
            self.show_error("All fields are required.")
            return

        # Validate numeric fields
        try:
            mileage = int(mileage)
            daily_price = float(daily_price)
            maintenance_cost = float(maintenance_cost)
        except ValueError:
            self.show_error("Invalid input for mileage, daily price, or maintenance cost.")
            return

        self.system.add_vehicle(brand, model, mileage, daily_price, maintenance_cost)
        self.show_info("Vehicle added successfully!")

        dialog.destroy()
        self.load_vehicles()