import pickle
import os

DB_NAME = "database.pkl"               # Define the name of the database file name

def load_data():
    if os.path.exists(DB_NAME):
        with open(DB_NAME, "rb") as f:
            return pickle.load(f)
    return { "counters": { "vehicles": 0, "bookings": 0, "logs": 0 }, "tables": { "vehicles": [], "bookings": [], "logs": [] }}

def save_data(data):
    with open(DB_NAME, "wb") as f:
        pickle.dump(data, f)