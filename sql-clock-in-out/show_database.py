import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('timesheet.db')
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM employees")  # Adjust the query based on your actual table structure
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
