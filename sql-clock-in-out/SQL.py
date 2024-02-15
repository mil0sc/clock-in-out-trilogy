import sqlite3


def setup_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

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


# Example usage, if needed
if __name__ == "__main__":
    setup_database('timesheet.db')
