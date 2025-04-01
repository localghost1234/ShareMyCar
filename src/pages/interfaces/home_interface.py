import sys

class HomeInterface():
    """
        A class with a simple visual representation for welcoming the user.
        Only used on application's startup.
    """
    def __init__(self, on_switch_interface, system):
        # Displays simple strings of messages, with varying types of letter and sizes
        print("Welcome to the car sharing management system!")

        interface_number = -1
        
        while interface_number < 1 and interface_number > 7:
            interface_number = input("Please select a valid operation (1-7):\n"
                "1) Check Vehicle Inventory\n"
                "2) Book A Vehicle\n"
                "3) Return A Vehicle\n"
                "4) Check Vehicle Maintenance\n"
                "5) Check Logs\n"
                "6) Check Financial Metrics\n"
            )

        on_switch_interface(interface_number)

