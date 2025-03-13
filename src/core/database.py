# database.py
import sqlite3

from src.misc.constants import DATABASE_TABLES_STATEMENTS, DB_NAME

class Database():
    def __init__(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        # Create the vehicles table
        for statement in DATABASE_TABLES_STATEMENTS:
            self.cursor.execute(statement)

        # Commit the changes and close the connection
        self.conn.commit()

    def execute_query(self, statement, params=()):
        self.cursor.execute(statement, params)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        try:
            # Commit any pending transactions
            self.conn.commit()
        except Exception as e:
            print(f"Error committing transactions: \n{e}")

        try:
            self.cursor.close()
        except Exception as e:
            print(f"Error closing the cursor: \n{e}")
        
        try:
            # Close the database connection
            self.conn.close()
        except Exception as e:
            print(f"Error closing the database connection: \n{e}")