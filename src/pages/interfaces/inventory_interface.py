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

        # Scrollbars (vertical and horizontal)
        self.v_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.VERTICAL)
        self.h_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.HORIZONTAL)

        # Text widget with both scrollbars
        self.inventory_text = tk.Text(
            self.vehicle_frame, height=15, width=70, wrap="none",
            yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set
        )

        # Pack elements properly
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.inventory_text.pack(fill=tk.BOTH, expand=True)

        # Link scrollbars
        self.v_scrollbar.config(command=self.inventory_text.yview)
        self.h_scrollbar.config(command=self.inventory_text.xview)

        self.load_vehicles()

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

    def load_vehicles(self):
        """Fetches and displays all vehicles in the inventory."""
        self.inventory_text.config(state=tk.NORMAL)
        self.inventory_text.delete("1.0", tk.END)

        vehicles = self.system.get_all_vehicles()
        
        if vehicles:
            for v in vehicles:
                vehicle_info = (
                    f"ID: {v[0]}\t\t"
                    f"Brand: {v[1]}\t\t"
                    f"Model: {v[2]}\t\t"
                    f"Current Mileage: {v[3]} miles\t\t"
                    f"Next Maintenance: {v[4]} miles\t\t"
                    f"Daily Price: €{v[5]}\t\t"
                    f"Maintenance Cost: €{v[6]}/mile\t\t"
                    f"Available: {'Yes' if v[7] else 'No'}\n"
                )
                self.inventory_text.insert(tk.END, vehicle_info)
        else:
            self.inventory_text.insert(tk.END, "No vehicles available.")

        self.inventory_text.config(state=tk.DISABLED)


