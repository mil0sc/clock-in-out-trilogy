import sqlite3
import logging
import datetime


class TimesheetError(Exception):
    """Custom exception class for timesheet-related errors."""
    pass


def connect_to_db(db_file):
    """Create a database connection."""
    return sqlite3.connect(db_file)


'''
def get_employee(db_file, employee_id=None, name=None):
    conn = connect_to_db(db_file)
    cursor = conn.cursor()

    if employee_id:
        cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    elif name:
        cursor.execute('SELECT * FROM employees WHERE name = ?', (name,))
    else:
        return None

    employee = cursor.fetchone()
    conn.close()
    return employee
'''
'''
def update_employee(db_file, employee_id, name=None, shift_hours=None):
    conn = connect_to_db(db_file)
    cursor = conn.cursor()

    if name and shift_hours:
        cursor.execute('UPDATE employees SET name = ?, shift_hours = ? WHERE id = ?', (name, shift_hours, employee_id))
    elif name:
        cursor.execute('UPDATE employees SET name = ? WHERE id = ?', (name, employee_id))
    elif shift_hours:
        cursor.execute('UPDATE employees SET shift_hours = ? WHERE id = ?', (shift_hours, employee_id))

    conn.commit()
    conn.close()
'''


def read_time_entries(db_file, employee_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM time_entries WHERE employee_id = ?", (employee_id,))
        entries = cursor.fetchall()
        return entries
    except sqlite3.Error as e:
        logging.error(f"SQL error while reading time entries: {e}")
        raise TimesheetError("Failed to read time entries due to a database error.")
    finally:
        conn.close()


def does_employee_exist(db_file, employee_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM employees WHERE id = ?", (employee_id,))
        employee = cursor.fetchone()
        return employee is not None
    except sqlite3.Error as e:
        logging.error(f"SQL error while checking if employee exists: {e}")
        raise TimesheetError("Failed to check if employee exists due to a database error.")
    finally:
        conn.close()


def get_employee_shift(db_file, employee_id):
    """Get the assigned shift for a given employee."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT shift_hours FROM employees WHERE id = ?", (employee_id,))
        shift_info = cursor.fetchone()
        if shift_info:
            return shift_info[0].strip()  # Extracts the shift, e.g., '(6-14)'
        else:
            return None  # Employee not found or no shift assigned
    except sqlite3.Error as e:
        logging.error(f"SQL error while reading shift information for employee {employee_id}: {e}")
        raise Exception(f"Error reading employee shift information: {e}")
    finally:
        conn.close()


def save_time_entry(db_file, employee_id, action):
    # Validate employee_id and action
    if not isinstance(employee_id, str) or not employee_id.strip():
        raise ValueError("Invalid employee ID provided.")

    valid_actions = ['IN', 'OUT']
    if action not in valid_actions:
        raise ValueError("Invalid action. Must be 'IN' or 'OUT'.")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Prepare SQL query to insert the time entry
        sql = "INSERT INTO time_entries (employee_id, timestamp, action) VALUES (?, ?, ?)"
        timestamp = datetime.datetime.now()

        # Execute the SQL query
        cursor.execute(sql, (employee_id, timestamp, action))

        # Commit the changes to the database
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"SQL error while saving time entry: {e}")
        raise TimesheetError(f"Failed to save time entry due to a database error: {e}")
    finally:
        # Ensure that the database connection is closed
        conn.close()


def generate_report(db_file, employee_id=None):
    """
    Generate a timesheet report for an employee or for all employees.
    Prints entries with employee names if they exist.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        if employee_id:
            # Generate report for a specific employee
            sql = '''
                SELECT employees.name, time_entries.timestamp, time_entries.action
                FROM time_entries
                JOIN employees ON employees.id = time_entries.employee_id
                WHERE employees.id = ?
            '''
            cursor.execute(sql, (employee_id,))
        else:
            # Generate report for all employees
            sql = '''
                SELECT employees.name, time_entries.timestamp, time_entries.action
                FROM time_entries
                JOIN employees ON employees.id = time_entries.employee_id
            '''
            cursor.execute(sql)

        entries = cursor.fetchall()
        if not entries:
            logging.info("No entries found for the report.")
            return []

        return entries

    except sqlite3.Error as e:
        logging.error(f"SQL error while generating report: {e}")
        raise TimesheetError("Failed to generate report due to a database error.")
    finally:
        conn.close()
