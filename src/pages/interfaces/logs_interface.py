import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.strings import LOGS

class LogsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *LOGS.TITLES)

        # Create a scrollable Listbox
        self.create_scrollable_listbox(LOGS.HEADERS)

        # Load transaction logs
        self.load_content(
            get_content=self.system.get_transaction_logs,
            generate_model=LOGS.GENERATE_MODEL,
            empty_message=LOGS.EMPTY_MESSAGE,
        )