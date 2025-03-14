import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.strings import MAINTENANCE

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *MAINTENANCE.TITLES)

        # Create a scrollable Listbox
        self.create_scrollable_listbox(MAINTENANCE.HEADERS)

        # Load vehicles requiring maintenance
        self.load_content(
            get_content=self.system.get_vehicles_requiring_maintenance,
            generate_model=MAINTENANCE.GENERATE_MODEL,
            empty_message=MAINTENANCE.EMPTY_MESSAGE,
        )