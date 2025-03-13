import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

titles = ("Logs Management", "Transaction Logs")
headers = ("Transaction ID", "Vehicle ID", "Customer Name", "Rental Duration (days)", "Revenue (€)", "Additional Costs (€)", "Transaction Type")
empty_message = "No transaction logs found."

generate_model = lambda content: (
    f"{content[0]:<15} | "
    f"{content[1]:<15} | "
    f"{content[5]:<15} | "
    f"{content[2]:<15} | "
    f"€{content[3]:<15} | "
    f"€{content[4]:<15} | "
    f"{content[6]:<15}"
)

class LogsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        # Create a scrollable Listbox
        self.create_scrollable_listbox(headers)

        # Load transaction logs
        self.load_content(
            get_content=self.system.get_transaction_logs,
            generate_model=generate_model,
            empty_message=empty_message,
        )