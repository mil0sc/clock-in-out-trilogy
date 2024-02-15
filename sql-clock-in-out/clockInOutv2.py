import datetime
import logging
from db_utils import (read_time_entries, get_employee_shift, does_employee_exist, save_time_entry)


class TimesheetError(Exception):
    """Custom exception class for timesheet-related errors."""
    pass


# Configure logging
logging.basicConfig(filename='timesheet.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def calculate_hours(db_file, employee_id):
    entries = read_time_entries(db_file, employee_id)
    total_seconds = 0
    last_clock_in = None

    for entry in entries:
        action_time = datetime.datetime.fromisoformat(entry[2])  # Assuming entry[2] is the timestamp
        action = entry[3]  # Assuming entry[3] is the action ('IN' or 'OUT')

        if action == 'IN':
            last_clock_in = action_time
        elif action == 'OUT' and last_clock_in:
            total_seconds += (action_time - last_clock_in).total_seconds()
            last_clock_in = None

    return total_seconds / 3600


def last_employee_action(db_file, employee_id):
    try:
        entries = read_time_entries(db_file, employee_id)
        if not entries:
            return None
        last_entry = entries[-1]
        if len(last_entry) < 4 or last_entry[3] not in ['IN', 'OUT']:
            raise ValueError("Invalid last entry format.")
        return last_entry[3]  # Assuming the action ('IN' or 'OUT') is in last_entry[3]
    except ValueError as e:
        logging.error(f"Error retrieving last action for employee {employee_id}: {e}")
        raise


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


def clock_in(db_file, employee_id):
    """Clock in an employee if their shift matches the current time, and they are not already clocked in."""
    if not does_employee_exist(db_file, employee_id):
        raise ValueError(f"Employee {employee_id} not found.")

    shift_hours = get_employee_shift(db_file, employee_id)
    if shift_hours is None:
        raise ValueError(f"Shift not assigned for employee {employee_id}.")

    current_hour = datetime.datetime.now().hour
    if not is_within_shift(shift_hours, current_hour):
        raise ValueError(f"Employee {employee_id} cannot clock in during this shift ({shift_hours}).")

    last_action = last_employee_action(db_file, employee_id)
    if last_action == 'IN':
        raise ValueError(f"Employee {employee_id} is already clocked in.")

    save_time_entry(db_file, employee_id, 'IN')


def clock_out(db_file, employee_id):
    """Clock out an employee."""
    save_time_entry(db_file, employee_id, 'OUT')


def try_clock_in(db_file, employee_id):
    try:
        clock_in(db_file, employee_id)
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


def try_clock_out(db_file, employee_id):
    try:
        clock_out(db_file, employee_id)
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
