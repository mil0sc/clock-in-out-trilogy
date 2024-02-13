import csv

admin_password = "admin"  # Set your admin password here


def check_admin_password(password):
    """Check if the provided password matches the admin password."""
    return password == admin_password


def format_name(name):
    """Format the name to have the first letter capitalized in each part."""
    return ' '.join(word.capitalize() for word in name.split())


def add_employee_to_csv(employee_name, shift_hours):
    """Add a new employee with their shift to the CSV file."""
    with open('employees.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([employee_name, shift_hours])


def get_shift_hours(shift_number):
    """Get shift hours based on shift number."""
    shifts = {
        'first': '(6-14)',
        'second': '(14-22)',
        'third': '(22-6)'
    }
    return shifts.get(shift_number)


def main():
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
        add_employee_to_csv(formatted_name, shift_hours)
        print(f"Added {formatted_name} with shift {shift_hours} to the CSV file.")


if __name__ == "__main__":
    main()
