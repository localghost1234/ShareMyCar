import pickle
import os

DB_NAME = "database.pkl"                                # Define the name of the database file name to avoid errors

def load_data():
    """Initialized database configuration and searches if any exists already. Otherwise, we create it."""
    if os.path.exists(DB_NAME):
        with open(DB_NAME, "rb") as f:
            return pickle.load(f)
    return { "counters": { "vehicles": 0, "bookings": 0, "logs": 0 }, "tables": { "vehicles": [], "bookings": [], "logs": [] }}

def save_data(data):
    """Receives new content and adds it to the database.
    
        Args:
        - data (Dictionary): Structure of data with either added or deleted information.
    """
    with open(DB_NAME, "wb") as f:
        pickle.dump(data, f)