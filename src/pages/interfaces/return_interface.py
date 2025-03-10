import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class ReturnInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, "Return Management", "Unavailable Vehicles")

        # Create a scrollable Listbox
        self.vehicle_listbox = self.create_scrollable_listbox(disable_clicking=False)

        # Load unavailable vehicles
        self.load_unavailable_vehicles()

        # Bind double-click event to handle vehicle selection
        self.vehicle_listbox.bind("<Double-Button-1>", self.on_vehicle_double_click)

    def load_unavailable_vehicles(self):
        """Fetches and displays all unavailable vehicles."""
        self.vehicle_listbox.delete(0, tk.END)  # Clear the listbox

        vehicles = self.system.get_unavailable_vehicles()  # Fetch unavailable vehicles
        
        if vehicles:
            # Define column headers
            headers = ["ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost", "Available"]
            header_row = (
                f"{headers[0]:<5} | "
                f"{headers[1]:<15} | "
                f"{headers[2]:<15} | "
                f"{headers[3]:<10} | "
                f"{headers[4]:<15} | "
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
                    f"{v[3]:<10} | "
                    f"€{v[4]:<9} | "
                    f"€{v[5]:<14} | "
                    f"{'No' if v[6] == 0 else 'Yes':<10}"
                )
                self.vehicle_listbox.insert(tk.END, vehicle_info)
        else:
            self.vehicle_listbox.insert(tk.END, "No unavailable vehicles found.")

    def on_vehicle_double_click(self, event):
        """Handles double-clicking on a vehicle in the list."""
        selected_index = self.vehicle_listbox.curselection()  # Get the selected item index
        if selected_index:
            selected_vehicle = self.vehicle_listbox.get(selected_index)  # Get the selected vehicle info
            vehicle_id = int(selected_vehicle.split(" | ")[0].strip())  # Extract the vehicle ID
            self.show_return_dialog(vehicle_id)  # Open the return dialog

    def show_return_dialog(self, vehicle_id):
        """Opens the return vehicle dialog with the selected vehicle's ID."""
        customer_name = self.system.get_customer_name(vehicle_id)  # Fetch customer name

        dialog = tk.Toplevel(self.root)
        dialog.title("Return Vehicle")
        dialog.geometry("300x200")

        # Vehicle ID (read-only)
        tk.Label(dialog, text="Vehicle ID:").grid(row=0, column=0, padx=10, pady=5)
        vehicle_id_entry = tk.Entry(dialog)
        vehicle_id_entry.insert(0, str(vehicle_id))
        vehicle_id_entry.config(state=tk.DISABLED)
        vehicle_id_entry.grid(row=0, column=1, padx=10, pady=5)

        # Customer Name (read-only)
        tk.Label(dialog, text="Customer Name:").grid(row=1, column=0, padx=10, pady=5)
        customer_name_entry = tk.Entry(dialog)
        customer_name_entry.insert(0, customer_name)
        customer_name_entry.config(state=tk.DISABLED)
        customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Kilometers Driven
        tk.Label(dialog, text="Kilometers Driven:").grid(row=2, column=0, padx=10, pady=5)
        actual_km_entry = tk.Entry(dialog)
        actual_km_entry.grid(row=2, column=1, padx=10, pady=5)

        # Late Days
        tk.Label(dialog, text="Late Days:").grid(row=3, column=0, padx=10, pady=5)
        late_days_entry = tk.Entry(dialog)
        late_days_entry.grid(row=3, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(
            dialog, text="Submit",
            command=lambda: self.submit_return(
                vehicle_id, actual_km_entry.get(), late_days_entry.get(), customer_name, dialog
            )
        )
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_return(self, vehicle_id, actual_km, late_days, customer_name, dialog):
        """Validates and submits the return details."""
        try:
            actual_km = int(actual_km)
            late_days = int(late_days)
        except ValueError:
            self.show_error("Please enter valid numbers for kilometers and late days.")
            return

        # Calculate total cost
        total_cost = self.system.query_return(vehicle_id, actual_km, late_days, customer_name)
        if total_cost:
            self.show_info(f"Vehicle returned! Total cost: €{total_cost}")
            dialog.destroy()
            self.load_unavailable_vehicles()  # Refresh the list
        else:
            self.show_error("Vehicle not found or already returned.")