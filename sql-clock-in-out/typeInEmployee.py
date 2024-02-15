import sqlite3

admin_password = "admin"  # Set your admin password here


def check_admin_password(password):
    """Check if the provided password matches the admin password."""
    return password == admin_password


def format_name(name):
    """Format the name to have the first letter capitalized in each part."""
    return ' '.join(word.capitalize() for word in name.split())


def add_employee_to_db(db_file, employee_name, shift_hours):
    """Add a new employee with their shift to the database."""
    conn = sqlite3.connect(db_file)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, shift_hours) VALUES (?, ?)", (employee_name, shift_hours))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding employee to the database: {e}")
    finally:
        conn.close()


def get_shift_hours(shift_number):
    """Get shift hours based on shift number."""
    shifts = {
        'first': '(6-14)',
        'second': '(14-22)',
        'third': '(22-6)'
    }
    return shifts.get(shift_number)


def main():
    db_file = 'timesheet.db'  # Path to your SQLite database file
    admin_input = input("Enter admin password to add a new employee: ")
    if not check_admin_password(admin_input):
        print("Incorrect admin password. Access denied.")
        return

    while True:
        employee_name = input("Enter the employee's name (or type 'exit' to quit): ")
        if employee_name.lower() == 'exit':
            break

        shift_number = input("Enter the employee's shift (first (6-14), second (14-22), third (22-6)): ").lower()
        shift_hours = get_shift_hours(shift_number)
        if not shift_hours:
            print("Invalid shift entered. Please try again.")
            continue

        formatted_name = format_name(employee_name)
        add_employee_to_db(db_file, formatted_name, shift_hours)
        print(f"Added {formatted_name} with shift {shift_hours} to the database.")


if __name__ == "__main__":
    main()
