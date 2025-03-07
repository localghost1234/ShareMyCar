import tkinter as tk
from tkinter import messagebox

from src.pages.interfaces.base_interface import BaseInterface

class ReturnInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Return Management", system)

        self.return_button = tk.Button(self.frame, text="Return Vehicle", command=self.show_return_dialog)
        self.return_button.pack()

    def show_return_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Return Vehicle")

        tk.Label(dialog, text="Vehicle ID:").grid(row=0, column=0)
        vehicle_id_entry = tk.Entry(dialog)
        vehicle_id_entry.grid(row=0, column=1)

        tk.Label(dialog, text="Kilometers Driven:").grid(row=1, column=0)
        actual_km_entry = tk.Entry(dialog)
        actual_km_entry.grid(row=1, column=1)

        tk.Label(dialog, text="Late Days:").grid(row=2, column=0)
        late_days_entry = tk.Entry(dialog)
        late_days_entry.grid(row=2, column=1)

        def submit():
            try:
                vehicle_id = int(vehicle_id_entry.get())
                actual_km = int(actual_km_entry.get())
                late_days = int(late_days_entry.get())

                total_cost = self.system.query_return(vehicle_id, actual_km, late_days)
                dialog.destroy()

                if total_cost:
                    messagebox.showinfo("Success", f"Vehicle returned! Total cost: €{total_cost}")
                else:
                    messagebox.showerror("Error", "Vehicle not found.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")

        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.grid(row=3, column=0, columnspan=2)
