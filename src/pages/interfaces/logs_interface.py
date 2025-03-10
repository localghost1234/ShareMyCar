import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class LogsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Transaction Logs", system)

        tk.Label(self.frame, text="Transaction Logs:").pack()

        # Frame for logs with scrollbars
        self.logs_frame = tk.Frame(self.frame)
        self.logs_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars (vertical and horizontal)
        self.v_scrollbar = tk.Scrollbar(self.logs_frame, orient=tk.VERTICAL)
        self.h_scrollbar = tk.Scrollbar(self.logs_frame, orient=tk.HORIZONTAL)

        # Listbox for displaying logs
        self.logs_listbox = tk.Listbox(
            self.logs_frame, height=15, width=100,
            font=("Courier", 10),
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )

        # Pack elements properly
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.logs_listbox.pack(fill=tk.BOTH, expand=True)

        # Link scrollbars
        self.v_scrollbar.config(command=self.logs_listbox.yview)
        self.h_scrollbar.config(command=self.logs_listbox.xview)

        # Load logs
        self.load_logs()

    def load_logs(self):
        """Fetches and displays transaction logs from the database."""
        self.logs_listbox.delete(0, tk.END)  # Clear previous entries

        logs = self.system.get_transaction_logs()

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
            self.logs_listbox.insert(tk.END, header_row)
            self.logs_listbox.insert(tk.END, "-" * 100)  # Insert separator line

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