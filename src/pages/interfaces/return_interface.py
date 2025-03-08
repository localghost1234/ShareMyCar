import tkinter as tk
from tkinter import messagebox
from src.pages.interfaces.base_interface import BaseInterface

class ReturnInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Return Management", system)

        tk.Label(self.frame, text="Unavailable Vehicles:").pack()

        # Frame for vehicle list with scrollbars
        self.vehicle_frame = tk.Frame(self.frame)
        self.vehicle_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars (vertical)
        self.v_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.VERTICAL)

        # Listbox to display vehicles
        self.vehicle_listbox = tk.Listbox(
            self.vehicle_frame, height=15, width=100,
            yscrollcommand=self.v_scrollbar.set, font=("Courier", 10)  # Use a monospaced font for alignment
        )

        # Pack elements properly
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vehicle_listbox.pack(fill=tk.BOTH, expand=True)

        # Link scrollbar
        self.v_scrollbar.config(command=self.vehicle_listbox.yview)

        # Load unavailable vehicles
        self.load_unavailable_vehicles()

        # Bind double-click event to handle vehicle selection
        self.vehicle_listbox.bind("<Double-Button-1>", self.on_vehicle_double_click)

    def load_unavailable_vehicles(self):
        """Fetches and displays all unavailable vehicles."""
        self.vehicle_listbox.delete(0, tk.END)  # Clear the listbox

        vehicles = self.system.get_unavailable_vehicles()  # Add this method to your system class
        
        if vehicles:
            # Define column headers
            headers = ["ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost"]
            header_row = (
                f"{headers[0]:<5} | "
                f"{headers[1]:<15} | "
                f"{headers[2]:<15} | "
                f"{headers[3]:<10} | "
                f"{headers[4]:<15} | "
                f"{headers[5]:<10} | "
                f"{headers[6]:<15}"
            )
            self.vehicle_listbox.insert(tk.END, header_row)  # Insert headers
            self.vehicle_listbox.insert(tk.END, "-" * 100)  # Insert a separator line

            for v in vehicles:
                vehicle_info = (
                    f"{v[0]:<5} | "
                    f"{v[1]:<15} | "
                    f"{v[2]:<15} | "
                    f"{v[3]:<10} | "
                    f"{v[4]:<15} | "
                    f"€{v[5]:<9} | "
                    f"€{v[6]:<14}"
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
        dialog = tk.Toplevel(self.root)
        dialog.title("Return Vehicle")

        tk.Label(dialog, text="Vehicle ID:").grid(row=0, column=0)
        vehicle_id_entry = tk.Entry(dialog)
        vehicle_id_entry.insert(0, str(vehicle_id))
        vehicle_id_entry.config(state=tk.DISABLED) 
        vehicle_id_entry.grid(row=0, column=1)

        tk.Label(dialog, text="Kilometers Driven:").grid(row=1, column=0)
        actual_km_entry = tk.Entry(dialog)
        actual_km_entry.grid(row=1, column=1)

        tk.Label(dialog, text="Late Days:").grid(row=2, column=0)
        late_days_entry = tk.Entry(dialog)
        late_days_entry.grid(row=2, column=1)

        def submit():
            try:
                actual_km = int(actual_km_entry.get())
                late_days = int(late_days_entry.get())

                total_cost = self.system.query_return(vehicle_id, actual_km, late_days)
                dialog.destroy()

                if total_cost:
                    messagebox.showinfo("Success", f"Vehicle returned! Total cost: €{total_cost}")
                    self.load_unavailable_vehicles()  # Refresh the list after returning
                else:
                    messagebox.showerror("Error", "Vehicle not found.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")

        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.grid(row=3, column=0, columnspan=2)