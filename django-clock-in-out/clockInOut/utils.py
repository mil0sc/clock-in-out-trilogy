# clockInOut/utils.py

import datetime
from .models import Employee, TimeEntry
from django.utils import timezone


def calculate_hours(employee_id):
    entries = TimeEntry.objects.filter(employee=employee_id).order_by('clock_in')
    total_seconds = 0
    last_clock_in = None

    for entry in entries:
        if entry.clock_in and entry.clock_out:
            if last_clock_in is None:
                last_clock_in = entry.clock_in
            if entry.clock_out:
                total_seconds += (entry.clock_out - last_clock_in).total_seconds()
                last_clock_in = None

    return total_seconds / 3600


def is_within_shift(shift_hours, current_hour):
    """Check if the current hour is within the given shift hours."""
    # Parse the shift_hours string to extract start and end hours
    start_hour, end_hour = map(int, shift_hours.strip("()").split('-'))

    # Adjust for shifts that span midnight (e.g., 22-6)
    if start_hour > end_hour:
        if current_hour >= start_hour or current_hour < end_hour:
            return True
    else:
        if start_hour <= current_hour < end_hour:
            return True


from django.utils import timezone
import datetime

def clock_in_employee(employee_id, work_category):
    # Check if the employee exists
    if not Employee.objects.filter(id=employee_id).exists():
        return "Error", f"Employee {employee_id} not found."

    try:
        employee = Employee.objects.get(id=employee_id)

        # Ensure the employee is assigned a shift
        if not employee.shift_hours:
            return "Error", "Shift not assigned for employee."

        # Check if the current time is within the shift
        if not is_within_shift(employee.shift_hours, datetime.datetime.now().hour):
            return "Error", "Not within shift hours."

        # Check the last action
        last_entry = TimeEntry.objects.filter(employee=employee).order_by('-clock_in').first()
        if last_entry and not last_entry.clock_out:
            return "Error", "Employee is already clocked in."

        # Clock in the employee with the specified work category
        TimeEntry.objects.create(
            employee=employee,
            clock_in=datetime.datetime.now(),
            work_category=work_category  # Include the work_category here
        )
        return "Success", f"Employee {employee_id} clocked in."

    except Employee.DoesNotExist:
        return "Error", f"Employee {employee_id} not found."


def clock_out_employee(employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)

        # Check the last action
        last_entry = TimeEntry.objects.filter(employee=employee).order_by('-clock_in').first()
        if last_entry and last_entry.clock_out is None:
            # Update the last entry with the clock-out time
            last_entry.clock_out = timezone.now()
            last_entry.save()
            return "Success", f"Employee {employee_id} clocked out."
        else:
            return "Error", "Employee is either not clocked in or already clocked out."

    except Employee.DoesNotExist:
        return "Error", f"Employee {employee_id} not found."


'''def can_employee_clock_in(employee):
    last_entry = TimeEntry.objects.filter(employee=employee).order_by('-clock_in').first()
    if last_entry and not last_entry.clock_out:
        return False
    return True
'''
'''
def clock_in_employee(employee):
    if can_employee_clock_in(employee):
        TimeEntry.objects.create(employee=employee, clock_in=timezone.now())
        return "Clock-in successful"
    else:
        return "Employee must clock out before clocking in again"
'''
