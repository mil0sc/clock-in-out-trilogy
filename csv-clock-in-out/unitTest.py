import csv
import datetime
import random
import unittest
from unittest.mock import patch, mock_open, ANY
from clockInOutv2 import calculate_hours, does_employee_exist, save_time_entry, read_time_entries, last_employee_action, \
    get_employee_shift, clock_in, timesheet_file, TimesheetError  # Add TimesheetError to the import list


class TestTimeSheetFunctions(unittest.TestCase):

    def test_calculate_hours_with_incomplete_entries(self):
        employee_id = "test_employee"

        # Case 1: Missing OUT entry
        mock_data_missing_out = [
            ['test_employee', datetime.datetime(2021, 1, 1, 9, 0).isoformat(), 'IN']
        ]
        with patch('clockInOutv2.read_time_entries', return_value=mock_data_missing_out):
            hours_missing_out = calculate_hours(employee_id)
            self.assertEqual(hours_missing_out, 0)  # Expect 0 hours due to incomplete entry

        # Case 2: Missing IN entry
        mock_data_missing_in = [
            ['test_employee', datetime.datetime(2021, 1, 1, 17, 0).isoformat(), 'OUT']
        ]
        with patch('clockInOutv2.read_time_entries', return_value=mock_data_missing_in):
            hours_missing_in = calculate_hours(employee_id)
            self.assertEqual(hours_missing_in, 0)  # Expect 0 hours due to incomplete entry

    def test_clock_in_during_incorrect_shift(self):
        employee_id = "test_employee"
        # Mock get_employee_shift to return a shift that is not current
        with patch('clockInOutv2.get_employee_shift', return_value='(14-22)'):
            # Mock datetime to simulate current time outside the mocked shift
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 9)  # 9 AM, not in the 14-22 shift
                with self.assertRaises(ValueError):
                    clock_in(employee_id)

    def test_does_employee_exist_non_existent(self):
        non_existent_employee = "non_existent_id"
        with patch('builtins.open', mock_open(read_data="existing_employee\n")):
            result = does_employee_exist(non_existent_employee)
            self.assertFalse(result)

    def test_calculate_hours_random_input(self):
        for _ in range(100):  # Run the test 100 times with different data
            # Generate a random start hour (between 0 and 15)
            # This ensures there's enough room for a work duration of up to 8 hours without exceeding 23
            start_hour = random.randint(0, 15)

            # Generate a random duration (1 to 8 hours)
            duration = random.randint(1, 8)

            # Calculate end_hour, ensuring it does not exceed 23
            end_hour = start_hour + duration
            if end_hour > 23:
                end_hour = 23

            # Generate mock data
            mock_data = [
                ['test_employee', datetime.datetime(2021, 1, 1, start_hour, 0).isoformat(), 'IN'],
                ['test_employee', datetime.datetime(2021, 1, 1, end_hour, 0).isoformat(), 'OUT']
            ]

            with patch('clockInOutv2.read_time_entries', return_value=mock_data):
                hours = calculate_hours('test_employee')
                # Calculate expected hours, considering the adjustment for end_hour
                expected_hours = min(duration, 23 - start_hour)
                self.assertEqual(hours, expected_hours)

    def test_save_time_entry(self):
        employee_id = "test_employee"
        action = "IN"
        with patch('csv.writer') as mock_writer:
            save_time_entry(employee_id, action)
            mock_writer.return_value.writerow.assert_called_with([employee_id, ANY, action])  # ANY can be used from
            # unittest.mock to ignore datetime check

    def test_save_time_entry_invalid_file(self):
        employee_id = "test_employee"
        action = "IN"
        with patch("builtins.open", side_effect=IOError("File not accessible")):
            with self.assertRaises(TimesheetError) as context:
                save_time_entry(employee_id, action)
            self.assertEqual(str(context.exception), "Failed to save time entry due to an internal error.")

    def test_read_time_entries_no_entries_for_employee(self):
        employee_id = "nonexistent_employee"
        with patch("csv.reader", return_value=[]):
            result = read_time_entries(employee_id)
            self.assertEqual(result, [])

    def generate_report(self=None):
        """
        Generate a timesheet report for an employee or for all employees
        """
        if self:
            entries = read_time_entries(self)
        else:
            entries = []
            with open(timesheet_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    entries.append(row)

        if entries:  # Check if the list is not empty
            for entry in entries:
                print(entry)
        # If entries is empty, nothing is printed

    def test_does_employee_exist(self):
        # Mock the open function to simulate reading from 'employees.csv'
        mock_file_data = 'existing_employee\n'
        with patch('builtins.open', mock_open(read_data=mock_file_data)):
            self.assertTrue(does_employee_exist("existing_employee"))
            self.assertFalse(does_employee_exist("non_existing_employee"))

    def test_last_employee_action_no_previous(self):
        employee_id = "employee_no_action"
        with patch('clockInOutv2.read_time_entries', return_value=[]):
            result = last_employee_action(employee_id)
            self.assertIsNone(result)

    def test_get_employee_shift_non_existent(self):
        non_existent_employee = "non_existent_id"
        with patch('builtins.open', mock_open(read_data="existing_employee\n")):
            result = get_employee_shift(non_existent_employee)
            self.assertIsNone(result)

    # You can add more test methods for other functions like read_time_entries, save_time_entry, etc.


if __name__ == '__main__':
    unittest.main()
