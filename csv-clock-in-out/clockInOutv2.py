import csv
import datetime
import logging


class TimesheetError(Exception):
    """Custom exception class for timesheet-related errors."""
    pass


# Configure logging
logging.basicConfig(filename='timesheet.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# File name for CSV storage
timesheet_file = 'timesheet_data.csv'


def save_time_entry(employee_id, action):
    # Validate employee_id and action
    if not isinstance(employee_id, str) or not employee_id.strip():
        raise ValueError("Invalid employee ID provided.")

    valid_actions = ['IN', 'OUT']
    if action not in valid_actions:
        raise ValueError("Invalid action. Must be 'IN' or 'OUT'.")

    try:
        with open(timesheet_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([employee_id, datetime.datetime.now(), action])
    except IOError as e:
        logging.error(f"IOError while saving time entry: {e}")
        raise TimesheetError("Failed to save time entry due to an internal error.")



def read_time_entries(employee_id):
    try:
        with open(timesheet_file, mode='r') as file:
            reader = csv.reader(file)
            return [row for row in reader if row[0] == employee_id]
    except FileNotFoundError:
        logging.error("Timesheet file not found.")
        raise TimesheetError("Timesheet data is currently unavailable.")
    except csv.Error as e:
        logging.error(f"CSV error while reading time entries: {e}")
        raise TimesheetError("Failed to read time entries due to a data error.")


def calculate_hours(employee_id):
    entries = read_time_entries(employee_id)
    total_seconds = 0
    last_clock_in = None

    for entry in entries:
        try:
            if len(entry) < 3 or not entry[0] == employee_id:
                raise ValueError("Invalid entry format.")

            time = datetime.datetime.fromisoformat(entry[1])
            action = entry[2]

            if action not in ['IN', 'OUT']:
                raise ValueError("Invalid action in entry.")

            # rest of the code...
        except ValueError as e:
            logging.error(f"Error processing time data for employee {employee_id}: {e}")
            raise ValueError(f"Error processing time data for {employee_id}: {e}")

    return total_seconds / 3600



def generate_report(employee_id=None):
    """
    Generate a timesheet report for an employee or for all employees.
    Only prints entries if they exist.
    """
    if employee_id:
        entries = read_time_entries(employee_id)
    else:
        with open(timesheet_file, mode='r') as file:
            reader = csv.reader(file)
            entries = list(reader)

    if not entries:  # Check if the entries list is empty
        logging.info("No entries found for the report.")
        return "No entries to report."

    for entry in entries:
        print(entry)


def does_employee_exist(employee_id):
    try:
        employee_id_lower = employee_id.lower()
        with open('employees.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].lower() == employee_id_lower:
                    return True
        return False
    except FileNotFoundError:
        raise FileNotFoundError("Employee file not found.")
    except csv.Error as e:
        raise Exception(f"Error reading employee file: {e}")


def last_employee_action(employee_id):
    try:
        entries = read_time_entries(employee_id)
        if not entries:
            return None
        last_entry = entries[-1]
        if len(last_entry) < 3 or last_entry[2] not in ['IN', 'OUT']:
            raise ValueError("Invalid last entry format.")
        return last_entry[2]
    except ValueError as e:
        logging.error(f"Error retrieving last action for employee {employee_id}: {e}")
        raise



def get_employee_shift(employee_id):
    """Get the assigned shift for a given employee."""
    try:
        with open('employees.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].lower() == employee_id.lower():
                    return row[1].strip()  # Extracts the shift, e.g., '(6-14)'
    except Exception as e:
        logging.error(f"Error reading employee file for employee {employee_id}: {e}")
        raise Exception(f"Error reading employee file: {e}")


def is_within_shift(shift_hours, current_hour):
    """Check if the current hour is within the given shift hours."""
    shift_times = {
        '(6-14)': range(6, 14),
        '(14-22)': range(14, 22),
        '(22-6)': list(range(22, 24)) + list(range(0, 6))
    }

    is_within = current_hour in shift_times[shift_hours]

    # Log the result of the check
    logging.info(f"Checked shift {shift_hours} for hour {current_hour}: {'within' if is_within else 'outside'} shift")

    return is_within


def clock_in(employee_id):
    """Clock in an employee if their shift matches the current time, and they are not already clocked in."""
    last_action = last_employee_action(employee_id)

    # Check if the employee is already clocked in
    if last_action == 'IN':
        raise ValueError(f"Employee {employee_id} is already clocked in.")

    # Check if the employee exists and get their shift hours
    shift_hours = get_employee_shift(employee_id)
    if not shift_hours:
        raise ValueError(f"Employee {employee_id} not found or shift not assigned.")

    # Check if current time is within the employee's shift hours
    current_hour = datetime.datetime.now().hour
    if not is_within_shift(shift_hours, current_hour):
        raise ValueError(f"Employee {employee_id} cannot clock in during this shift ({shift_hours}).")

    # If all checks pass, save the time entry
    save_time_entry(employee_id, 'IN')


def clock_out(employee_id):
    save_time_entry(employee_id, 'OUT')


def try_clock_in(employee_id):
    try:
        clock_in(employee_id)
        return "Success", f"Employee {employee_id} clocked in."
    except ValueError as e:
        logging.error(f"Clock-in error for employee {employee_id}: {e}")
        return "Error", str(e)
    except TimesheetError as e:
        logging.error(f"Timesheet error during clock-in for employee {employee_id}: {e}")
        return "Error", "An error occurred while clocking in."
    except Exception as e:
        logging.error(f"Unexpected error during clock-in for employee {employee_id}: {e}")
        return "Error", "An unexpected error occurred: " + str(e)



def try_clock_out(employee_id):
    try:
        clock_out(employee_id)
        return "Success", f"Employee {employee_id} clocked out."
    except ValueError as e:
        logging.error(f"Clock-out error for employee {employee_id}: {e}")
        return "Error", str(e)
    except TimesheetError as e:
        logging.error(f"Timesheet error during clock-out for employee {employee_id}: {e}")
        return "Error", "An error occurred while clocking out."
    except Exception as e:
        logging.error(f"Unexpected error during clock-out for employee {employee_id}: {e}")
        return "Error", "An unexpected error occurred: " + str(e)
