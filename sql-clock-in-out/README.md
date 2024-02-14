## Timesheet Management System

### Overview

This **Timesheet Management System** is a sophisticated Python application designed to streamline employee time tracking and shift management. Built with a focus on simplicity and efficiency, the system integrates a user-friendly GUI with robust back-end database operations, making it ideal for small to medium-sized businesses or departments within larger organizations.

### Features

- **Clock In/Out Functionality:** <br>
Employees can clock in and out with ease, with each action meticulously logged to ensure accurate time tracking. 
- **Shift Management:** <br>
Admins can assign specific shifts to employees and ensure that clock-in actions are only valid during assigned shift hours. 
- **Time Calculations:** <br>
The system automatically calculates the total hours worked by an employee, providing essential data for payroll processing. 
- **Report Generation:** <br>
Generate detailed reports for individual employees or across the workforce, offering insights into work patterns and shift adherence. 
- **Employee Management:** <br>
Includes tools for adding new employees to the system, complete with name normalization and shift assignment. 
- **Database Migration:** <br>
A utility script to migrate existing employee data from CSV format into the system's SQLite database. 
- **Admin Controls:** <br>
Protected administrative functions for adding employees and generating reports, secured by a password.

### Technologies

- **Python:** <br>
The core programming language used to develop all functionalities of the system. 
- **Tkinter:** <br>
For creating the graphical user interface, enabling easy interaction with the system. 
- **SQLite:** <br>
A lightweight, disk-based database to store employee and time entry data, offering portability and ease of use. 
- **CSV:** <br>
Support for importing employee data from CSV files, facilitating easy data migration.

### Architecture

The system is organized into modular components for ease of maintenance and scalability:

- **main.py:** The entry point of the application, housing the GUI logic and user interaction workflows. 
- **clockInOutv2.py and db_utils.py:** These scripts encapsulate the business logic and database operations, respectively. 
- **typeInEmployee.py:** Contains utilities for managing employee data, including addition and shift management. 
- **migrate.py and SQL.py:** Scripts for database setup and data migration, ensuring that the system can be quickly initialized with existing data. 
- **timesheet.db:** An SQLite database file, serving as the persistent storage mechanism for all application data.

### Setup and Usage

To run the Timesheet Management System, ensure you have Python installed on your system. Clone the repository, navigate to the project directory, and execute python `main.py` to launch the application. Administrative functions require a predefined password, set within `typeInEmployee.py`.

### Potential Enhancements

Implementing more sophisticated authentication mechanisms for admin functions.
Expanding reporting capabilities to include analytics on overtime, absenteeism, and shift preferences.
Integration with payroll systems to automate salary computations based on hours worked.
