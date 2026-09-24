import sqlite3

class DAL:
    # UPDATE, INSERT, DELETE
    def no_output (self, query, db_path):
        try:
            with sqlite3.connect(db_path) as connection:
                connection.execute(query)
                connection.commit()
            return "operation was successfully !!!"
        except Exception as error:
            return f"Error: {error}"

    # SELECT
    def have_output (self, query, db_path):
        try:
            with sqlite3.connect(db_path) as connection:
                cursor = connection.cursor()
                resault = cursor.execute(query)
                rows = resault.fetchall()
            return rows
        except Exception as error:
            return f"Error: {error}"