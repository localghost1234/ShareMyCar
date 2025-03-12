import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

titles = ("Inventory Management", "All existing vehicles")
headers = ("ID", "Brand", "Model", "Mileage (kms)", "Daily Price", "Maintenance Cost", "Available")
empty_message = "No vehicles available."

generate_model = lambda content: (
    f"{content[0]:<13} | "
    f"{content[1]:<13} | "
    f"{content[2]:<13} | "
    f"{content[3]:<13} | "
    f"€{content[4]:<13} | "
    f"€{content[5]:<13} | "
    f"{'Yes' if content[6] else 'No':<13}"
)

class InventoryInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root,  system, *titles)

        self.create_scrollable_listbox(headers)

        self.load_content(
            get_content=self.system.get_all_vehicles,
            generate_model=generate_model,
            empty_message=empty_message,
        )

        self.add_button = tk.Button(self.frame, text="Add Vehicle", command=self.add_vehicle)
        self.add_button.pack(padx=10, pady=10)

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
        self.load_content(
            get_content=self.system.get_all_vehicles,
            generate_model=generate_model,
            empty_message=empty_message,
        )