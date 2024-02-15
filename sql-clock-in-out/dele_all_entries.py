import sqlite3

def setup_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                          id INTEGER PRIMARY KEY,
                          name TEXT NOT NULL,
                          shift_hours TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS time_entries (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          employee_id INTEGER NOT NULL,
                          timestamp DATETIME NOT NULL,
                          action TEXT NOT NULL,
                          FOREIGN KEY (employee_id) REFERENCES employees (id)
                      )''')

    conn.commit()
    conn.close()

def clear_all_data(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # SQL statement to delete all entries from both tables
    cursor.execute('DELETE FROM time_entries')  # Clear time_entries first due to foreign key constraint
    cursor.execute('DELETE FROM employees')  # Then clear employees

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    db_file = 'timesheet.db'
    setup_database(db_file)

    # Clear all entries from both the employees and time_entries tables
    clear_all_data(db_file)
    print("All entries in both 'employees' and 'time_entries' tables have been deleted.")
