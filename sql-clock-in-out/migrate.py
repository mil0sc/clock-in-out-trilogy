import csv
import sqlite3

def migrate_csv_to_sqlite(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Assuming each row in the CSV has two elements: name and shift_hours
            name, shift_hours = row

            # Insert data into the employees table
            cursor.execute('INSERT INTO employees (name, shift_hours) VALUES (?, ?)', (name.strip(), shift_hours.strip()))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_csv_to_sqlite('employees.csv', 'timesheet.db')
