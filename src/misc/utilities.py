import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

generate_header_row = lambda headers: "  |  ".join(f"{h:<15}" for h in headers)     # Creates a string of separated values from a list

def input_loop(on_validate_constraints, input_message):
    action_number = -1
    while on_validate_constraints(action_number):
        try:
            action_number = int(input(input_message))
        except ValueError:
            action_number = -1
    return action_number


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")  # "cls" for Windows, "clear" for Linux/macOS
