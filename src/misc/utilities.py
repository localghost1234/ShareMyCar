generate_row = lambda values: "| ".join(f"{v:<16}" for v in values)     # Creates a string of separated values from a list

def input_loop(on_validate_constraints, input_message):
    action_number = -1
    while on_validate_constraints(action_number):
        try:
            action_number = int(input(input_message))
        except ValueError:
            action_number = -1
    return action_number
