import csv
import random

# List of employee names to add
employee_names = ["Jakub", "Kacper", "Jan", "Antoni", "Michał",
                  "Szymon", "Filip", "Mateusz", "Paweł", "Adam", "Mateusz"]

# File name for employee storage
employee_file = 'employees.csv'

# Function to add employee names and their shifts to a CSV file
def add_employees(names, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        for name in names:
            # Randomly assign a shift to each employee
            shift = random.choice(["(6-14)", "(14-22)","(22-6)"])
            # Manually format and write the line to avoid CSV auto-quoting
            file.write(f"{name},{shift}\n")

# Adding the employees and their shifts to the file
add_employees(employee_names, employee_file)
