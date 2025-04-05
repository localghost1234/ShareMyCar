from src.misc.utilities import input_loop

class HomeInterface():
    """
        A class with a simple visual representation for welcoming the user.
        Only used on application's startup.
    """
    def __init__(self, on_switch_interface):
        # Displays simple strings of messages, with varying types of letter and sizes
        print("Welcome to the car sharing management system!")

        validator = lambda num: num < 1 or num > 6
        message = """Please select a valid operation (1-6):
            1) Check Vehicle Inventory
            2) Book A Vehicle
            3) Return A Vehicle
            4) Check Vehicle Maintenance
            5) Check Logs
            6) Check Financial Metrics

            """
        
        action_number = input_loop(validator, message)

        on_switch_interface(action_number)

