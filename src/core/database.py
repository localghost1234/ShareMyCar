import sqlite3                                                              # Import the sqlite3 library to interact with a lightweight database
from src.misc.constants import DATABASE_TABLE_STATEMENTS, DB_NAME, SQL      # Import constant strings for database table creation, database name, and SQL-related configurations

class Database():
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)        # Connect to the SQLite database (or create it if it doesn't exist)
        self.cursor = self.conn.cursor()            # Creates 'cursor' object, which helps us iterate over the data

        for statement in DATABASE_TABLE_STATEMENTS: # Iterates over a list of SQL statements with the tables the app uses
            self.cursor.execute(statement)          # Takes the statement strings, and applies them to the DB

        self.conn.commit()                          # Writes all changes into the database

    def execute_query(self, operation, table, columns=["*"], values=[], where="", fetch=SQL.FETCH.ALL):
        """
        Generalized method to execute SQL queries.
        
        :param operation: SQL operation (SELECT, INSERT, UPDATE, DELETE)
        :param table: Table name
        :param columns: Columns to select/insert/update (default is "*")
        :param values: Values for INSERT or UPDATE (tuple or list)
        :param where: WHERE clause (string)
        :param fetch: Whether to fetch one row or all rows (SQL.FETCH.ONE or SQL.FETCH.ALL)
        :return: Query result (for SELECT) or None
        """
        query = ""                                                                              # Initializes the string to be executed

        try:                                                                                    # Creates a scope where any possible error will get caught, to make debugging easier
            if operation == SQL.OPERATION.SELECT:                                               # Check if operation is SELECT
                query = f"SELECT {', '.join(columns)} FROM {table}"                             # Build SELECT query
            elif operation == SQL.OPERATION.INSERT:                                             # Check if operation is INSERT
                placeholders = ", ".join(["?"] * len(values))                                   # Create placeholders '?' to indicate where the values will be set
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"   # Build INSERT query
            elif operation == SQL.OPERATION.UPDATE:                                             # Check if operation is UPDATE
                set_clause = ", ".join([f"{col} = ?" for col in columns])                       # Creates string with columns to be changed
                query = f"UPDATE {table} SET {set_clause}"                                      # Build UPDATE query
            elif operation == SQL.OPERATION.DELETE:                                             # Check if operation is DELETE
                query = f"DELETE FROM {table}"                                                  # Build DELETE query

            if where:                                                                           # Checks if 'where' param is set to other than a falsy value
                query += f" WHERE {where}"                                                      # Adds WHERE clause to query, if 'where' is truthy

            self.cursor.execute(query, values) if values else self.cursor.execute(query)        # If 'values' is not a falsy value, it will be introduced into database query
        except Exception as err:                                                                # If any error arises during query creation or execution, all previous code is skipped to here
            print("Error during database querying ->", query)                                   # Prints message showcasing the query in its failing state
            print(err)                                                                          # Prints the error/exception
            raise Exception(err)                                                                # Sends error to any module using the 'execute_query()', in case developers wish to indicate its exact location

        if operation != SQL.OPERATION.SELECT:                                                   # Checks if the requested operation is not a 'SELECT'
            return None                                                                         # If true, returns nothing (since no value is expected)
        
        return self.cursor.fetchone() if fetch == SQL.FETCH.ONE else self.cursor.fetchall()     # Checks if request wants one or all the possible 'SELECT' values

    def commit(self):
        """
            Writes whatever changes have been done DB.
            This is done so to avoid direct usage of 'conn' variable outside of database.py
        """
        self.conn.commit()                              # Writes whatever changes have been done to DB

    def close(self):
        """
            Writes down all unsaved changes in DB,
            closes connection with both the cursor (iterator) object,
            and finally with the database itself.
        """
        try:
            self.conn.commit()                          # Write down any pending transactions to avoid data loss
            self.cursor.close()                         # Closes the iterator
            self.conn.close()                           # Closes the database connection
        except Exception as e:                          # If any error arises during any of these operations, it skips to this point
            print("Error closing the database\n", e)    # Displays error to developer consoles