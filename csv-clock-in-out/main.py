import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button, simpledialog

from clockInOutv2 import calculate_hours, clock_in, clock_out, read_time_entries, try_clock_in, try_clock_out
from typeInEmployee import format_name, add_employee_to_csv, get_shift_hours, \
    check_admin_password  # Import the function


# GUI functions
def gui_clock_in():
    employee_id = entry_employee_id.get()
    if employee_id:
        status, message = try_clock_in(employee_id)
        if status == "Success":
            messagebox.showinfo(status, message)
        else:
            messagebox.showerror(status, message)
    else:
        messagebox.showerror("Error", "Please enter an employee ID.")


def gui_clock_out():
    employee_id = entry_employee_id.get()
    if employee_id:
        status, message = try_clock_out(employee_id)
        if status == "Success":
            messagebox.showinfo(status, message)
        else:
            messagebox.showerror(status, message)
    else:
        messagebox.showerror("Error", "Please enter an employee ID.")


def gui_generate_report():
    employee_id = entry_employee_id.get()
    report_text.delete(1.0, tk.END)
    if employee_id:
        try:
            entries = read_time_entries(employee_id)
            for entry in entries:
                report_text.insert(tk.END, f"{entry}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {e}")
    else:
        messagebox.showerror("Error", "Please enter an employee ID.")


def gui_calculate_hours():
    employee_id = entry_employee_id.get()
    if employee_id:
        hours = calculate_hours(employee_id)
        messagebox.showinfo("Total Hours", f"Total hours for employee {employee_id}: {hours:.2f}")
    else:
        messagebox.showerror("Error", "Please enter an employee ID.")


def open_add_employee_window():
    admin_password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
    if not check_admin_password(admin_password):  # Use the imported function
        messagebox.showerror("Error", "Incorrect admin password. Access denied.")
        return

    add_window = Toplevel(root)  # Create a new window
    add_window.title("Add Employee")

    # Employee name entry
    Label(add_window, text="Employee's Name:").pack()
    name_entry = Entry(add_window)
    name_entry.pack()

    # Shift selection
    Label(add_window, text="Shift (first, second, third):").pack()
    shift_entry = Entry(add_window)
    shift_entry.pack()

    # Submit button
    submit_button = Button(add_window, text="Add Employee",
                           command=lambda: submit_add_employee(name_entry.get(), shift_entry.get(), add_window))
    submit_button.pack()


def submit_add_employee(name, shift, window):
    if not name or not shift:
        messagebox.showerror("Error", "All fields are required.")
        return

    shift_hours = get_shift_hours(shift.lower())
    if not shift_hours:
        messagebox.showerror("Error", "Invalid shift entered.")
        return

    formatted_name = format_name(name)
    add_employee_to_csv(formatted_name, shift_hours)
    messagebox.showinfo("Success", f"Added {formatted_name} with shift {shift_hours} to the CSV file.")
    window.destroy()  # Close the add employee window


# Create the main window
root = tk.Tk()
root.title("Timesheet Application")

# Create widgets
label_employee_id = tk.Label(root, text="Employee ID:")
entry_employee_id = tk.Entry(root)
button_clock_in = tk.Button(root, text="Clock In", command=gui_clock_in)
button_clock_out = tk.Button(root, text="Clock Out", command=gui_clock_out)
button_generate_report = tk.Button(root, text="Generate Report", command=gui_generate_report)
button_calculate_hours = tk.Button(root, text="Calculate Hours", command=gui_calculate_hours)
report_text = tk.Text(root, height=50, width=250)
button_add_employee = tk.Button(root, text="Add Employee", command=open_add_employee_window)
button_add_employee.pack()

# Arrange widgets in the main window
label_employee_id.pack()
entry_employee_id.pack()
button_clock_in.pack()
button_clock_out.pack()
button_generate_report.pack()
button_calculate_hours.pack()
report_text.pack()

# Run the application
root.mainloop()
