from tinydb import TinyDB, Query
from src.misc.constants import DB_NAME, SQL

class Database():
    def __init__(self):
        self.conn = TinyDB(DB_NAME, encoding='utf-8', ensure_ascii=False)  # Uses JSON file instead of SQLite
        self.tables = {
            SQL.TABLE.VEHICLES: self.conn.table(SQL.TABLE.VEHICLES),
            SQL.TABLE.BOOKINGS: self.conn.table(SQL.TABLE.BOOKINGS),
            SQL.TABLE.LOGS: self.conn.table(SQL.TABLE.LOGS)
        }
        self.query = Query()

    def execute_query(self, operation, table, columns=["*"], values=[], where="", fetch=SQL.FETCH.ALL):
        """
        TinyDB implementation of the generalized query method.
        Maintains the same interface as SQLite version.
        """
        try:
            table_obj = self.tables[table]
            result = None

            if operation == SQL.OPERATION.SELECT:
                # TinyDB doesn't support column selection natively
                if where:
                    if ">=" in where:
                        col, val = where.split(">=")
                        result = table_obj.search(self.query[col.strip()] >= float(val.strip()))
                    elif "=" in where:
                        col, val = where.split("=")
                        result = table_obj.search(self.query[col.strip()] == val.strip().strip("'"))
                else:
                    result = table_obj.all()

                # Filter columns if not "*"
                if columns != ["*"] and result:
                    result = [{k: v for k, v in item.items() if k in columns} for item in result]

            elif operation == SQL.OPERATION.INSERT:
                doc = dict(zip(columns, values))
                table_obj.insert(doc)
                return len(table_obj)  # Return new document count

            elif operation == SQL.OPERATION.UPDATE:
                updates = dict(zip(columns, values))
                if where and "=" in where:
                    col, val = where.split("=")
                    table_obj.update(updates, self.query[col.strip()] == val.strip().strip("'"))
                return None

            elif operation == SQL.OPERATION.DELETE:
                if where and "=" in where:
                    col, val = where.split("=")
                    table_obj.remove(self.query[col.strip()] == val.strip().strip("'"))
                return None

            # Handle fetch type
            if operation == SQL.OPERATION.SELECT:
                if fetch == SQL.FETCH.ONE:
                    return result[0] if result else None
                return result if result else []

        except Exception as err:
            print("Error during database operation ->", operation, table)
            print(err)
            raise Exception(err)

    def close(self):
        """TinyDB doesn't need explicit closing, but we'll flush writes"""
        self.conn.close()