# database.py
import sqlite3

from src.misc.constants import DATABASE_TABLE_STATEMENTS, DB_NAME, SQL

class Database():
    def __init__(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        # Create the vehicles table
        for statement in DATABASE_TABLE_STATEMENTS:
            self.cursor.execute(statement)

        # Commit the changes and close the connection
        self.conn.commit()

    def execute_query(self, operation, table, columns=["*"], values=[], where=[], fetch=SQL.FETCH.ALL):
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
        query = f"{operation} {", ".join(columns)} FROM {table}" if operation == SQL.OPERATION.SELECT else ""

        try:
            if operation == SQL.OPERATION.INSERT:
                placeholders = ", ".join(["?"] * len(values))
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            elif operation == SQL.OPERATION.UPDATE:
                set_clause = ", ".join([f"{col} = ?" for col in columns])
                query = f"UPDATE {table} SET {set_clause}"
            elif operation == SQL.OPERATION.DELETE:
                query = f"DELETE FROM {table}"

            if where:
                query += f" WHERE {where}"
        except Exception as e:
            print("Operational error, please ensure all params in 'execute_query()' are correct")
            print(e)

        try:
            self.cursor.execute(query, values) if values else self.cursor.execute(query)
        except Exception as e:
            print("Error during database query:", e)
            print("Query:", query)
            return None

        if operation != SQL.OPERATION.SELECT:
            return None
        
        return self.cursor.fetchone() if fetch == SQL.FETCH.ONE else self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

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