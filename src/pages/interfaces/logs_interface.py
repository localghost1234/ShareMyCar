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

        # Text widget with both scrollbars
        self.logs_text = tk.Text(
            self.logs_frame, height=15, width=70, wrap="none",
            yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set
        )

        # Pack elements properly
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.logs_text.pack(fill=tk.BOTH, expand=True)

        # Link scrollbars
        self.v_scrollbar.config(command=self.logs_text.yview)
        self.h_scrollbar.config(command=self.logs_text.xview)

        # Load logs
        self.load_logs()

    def load_logs(self):
        """Fetches and displays transaction logs from the database."""
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete("1.0", tk.END)

        logs = self.system.get_transaction_logs()

        if logs:
            for log in logs:
                log_entry = (
                    f"Transaction ID: {log[0]}\t"
                    f"Customer Name: {log[1]}\t"
                    f"Vehicle ID: {log[2]}\t"
                    f"Rental Duration: {log[3]} days\t"
                    f"Revenue: €{log[4]}\t"
                    f"Additional Costs: €{log[5]}\n"
                )
                self.logs_text.insert(tk.END, log_entry)
        else:
            self.logs_text.insert(tk.END, "No transaction logs available.")

        self.logs_text.config(state=tk.DISABLED)

