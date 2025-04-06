import pickle
import os

DB_NAME = "database.pkl"               # Define the name of the database file name

def load_data():
    if os.path.exists(DB_NAME):
        with open(DB_NAME, "rb") as f:
            return pickle.load(f)
    return {"vehicles": [], "bookings": [], "logs": []}

def save_data(data):
    with open(DB_NAME, "wb") as f:
        pickle.dump(data, f)

generate_row = lambda values: "| ".join(f"{v:<16}" for v in values)     # Creates a string of separated values from a list
