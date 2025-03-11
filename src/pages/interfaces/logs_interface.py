import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

headers = ("Transaction ID", "Vehicle ID", "Customer Name", "Rental Duration (days)", "Revenue (€)", "Additional Costs (€)")
header_row = " | ".join(f"{h:<15}" for h in headers)

generate_model = lambda content: (
    f"{content[0]:<15} | "
    f"{content[1]:<10} | "
    f"{content[6]:<20} | "
    f"{content[2]:<20} | "
    f"€{content[3]:<11} | "
    f"€{content[4]:<17}"
)

class LogsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, "Logs Management", "Transaction Logs")

        # Create a scrollable Listbox
        self.create_scrollable_listbox()

        # Load transaction logs
        self.load_content(
            get_content=self.system.get_transaction_logs,
            generate_model=generate_model,
            header_row=header_row,
            empty_message="No transaction logs found."
        )