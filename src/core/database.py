import os, pickle                                       # Import the Python default libraries 'os' (to interact with the PC) and 'pickle' a simple database system

DB_NAME = "database.pkl"                                # Define the name of the database file name to avoid discrepancies

def load_data():
    """Initialized database configuration and searches if any exists already. Otherwise, we create it."""
    if os.path.exists(DB_NAME):                                    # Checks if there's already an existing database in the current working directory
        with open(DB_NAME, "rb") as f:                             # If DB is found, it opens the file and gives reading permissions to it
            return pickle.load(f)                                  # Returns the data
    return { "counters": { "vehicles": 0, "bookings": 0, "logs": 0 }, "tables": { "vehicles": [], "bookings": [], "logs": [] }} # If no DB exists, a dictionary two dictionaries is returned: counters (to keep track of each table object's IDs), and tables (which carries almost all our needed data)

def save_data(data):
    """Receives new content and adds it to the database.
    
        Args:
        - data (Dictionary): Structure of data with either added or deleted information.
    """
    with open(DB_NAME, "wb") as f:                      # Opens channel to interact with the DB and gives writting permissions
        pickle.dump(data, f)                            # Stores new info and saves it