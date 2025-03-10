import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class LogsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, "Logs Management", "Transaction Logs")

        # Create a scrollable Listbox
        self.logs_listbox = self.create_scrollable_listbox()

        # Load transaction logs
        self.load_logs()

    def load_logs(self):
        """Fetches and displays transaction logs from the database."""
        self.logs_listbox.delete(0, tk.END)  # Clear the listbox

        logs = self.system.get_transaction_logs()  # Fetch logs
        
        if logs:
            # Define column headers
            headers = [
                "Transaction ID", "Vehicle ID", "Customer Name", "Rental Duration (days)",
                "Revenue (€)", "Additional Costs (€)"
            ]
            header_row = (
                f"{headers[0]:<15} | "
                f"{headers[1]:<10} | "
                f"{headers[2]:<20} | "
                f"{headers[3]:<20} | "
                f"{headers[4]:<12} | "
                f"{headers[5]:<18}"
            )
            self.logs_listbox.insert(tk.END, header_row)  # Insert headers
            self.logs_listbox.insert(tk.END, "-" * 100)  # Insert a separator line

            for log in logs:
                log_entry = (
                    f"{log[0]:<15} | "
                    f"{log[1]:<10} | "
                    f"{log[6]:<20} | "
                    f"{log[2]:<20} | "
                    f"€{log[3]:<11} | "
                    f"€{log[4]:<17}"
                )
                self.logs_listbox.insert(tk.END, log_entry)
        else:
            self.logs_listbox.insert(tk.END, "No transaction logs available.")