from django.urls import reverse
from django.test import TestCase
from clockInOut.models import Employee, TimeEntry
from clockInOut.utils import calculate_hours, clock_in_employee, clock_out_employee
from django.utils import timezone
import datetime
from rest_framework import status


class ClockInOutViewTests(TestCase):

    def test_clock_in_out_view_get(self):
        response = self.client.get(reverse('clock_in_out'))
        self.assertEqual(response.status_code, 200)

    def test_work_hours_view_get(self):
        response = self.client.get(reverse('calculate_hours'))
        self.assertEqual(response.status_code, 200)

    def test_generate_report_view_get(self):
        response = self.client.get(reverse('generate_report'))
        self.assertEqual(response.status_code, 200)

    def test_employee_list_view_get(self):
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, 200)

    def test_time_entries_list_view_get(self):
        response = self.client.get(reverse('time-entries-list'))
        self.assertEqual(response.status_code, 200)

    def test_main_dashboard_view_get(self):
        response = self.client.get(reverse('main-dashboard'))
        self.assertEqual(response.status_code, 200)


def test_predictions_view(self):
    url = reverse('predictions')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


def test_aggregated_predictions_api(self):
    url = reverse('aggregated_predictions_api')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


def test_company_targets_view(self):
    url = reverse('company-targets')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


def test_aggregated_predictions_view(self):
    url = reverse('aggregated_predictions')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


def test_calculated_hours_view(self):
    url = reverse('calculated-hours')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


def test_employee_hours_data(self):
    url = reverse('employee-hours-data')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

class UtilsTestCase(TestCase):
    def setUp(self):
        # Create test employee
        self.employee = Employee.objects.create(name="Test Employee", job_role="backend", shift_hours="9-17")
        # Create test time entries
        self.start_time = timezone.make_aware(datetime.datetime.now() - datetime.timedelta(hours=8))
        self.end_time = timezone.make_aware(datetime.datetime.now() - datetime.timedelta(hours=2))
        TimeEntry.objects.create(employee=self.employee, clock_in=self.start_time, clock_out=self.end_time)

    def test_calculate_hours(self):
        # Calculate hours for the test employee
        hours = calculate_hours(self.employee.id)
        self.assertTrue(hours > 0, "Hours should be greater than 0")

    def test_clock_in_employee(self):
        # Attempt to clock in the test employee
        status, message = clock_in_employee(self.employee.id, "Remote")
        self.assertEqual(status, "Success", "Employee should be clocked in successfully")

    def test_clock_out_employee(self):
        # Clock out the test employee
        status, message = clock_out_employee(self.employee.id)
        self.assertEqual(status, "Success", "Employee should be clocked out successfully")

    def test_is_within_shift(self):
        # You need to implement this test based on the `is_within_shift` function logic
        pass

    def tearDown(self):
        # Clean up code if needed
        pass


class ViewTestCase(TestCase):


    def test_clock_in_out_view_get(self):
        # The URL name for 'clock_in_out_view' is 'clock_in_out'
        response = self.client.get(reverse('clock_in_out'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_work_hours_view_get(self):
        # The URL name for 'work_hours_view' is 'calculate_hours'
        response = self.client.get(reverse('calculate_hours'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_report_view_get(self):
        # The URL name for 'generate_report_view' is 'generate_report'
        response = self.client.get(reverse('generate_report'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_view_get(self):
        # The URL name for 'employee_list_view' is 'employee-list'
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_time_entries_list_view_get(self):
        # The URL name for 'time_entries_list_view' is 'time-entries-list'
        response = self.client.get(reverse('time-entries-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_main_dashboard_view_get(self):
        # The URL name for 'main_dashboard' view is 'main-dashboard'
        response = self.client.get(reverse('main-dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # For API views, follow the same pattern
    def test_predictions_view_get(self):
        response = self.client.get(reverse('predictions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_aggregated_predictions_api_get(self):
        response = self.client.get(reverse('aggregated_predictions_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_targets_view_get(self):
        response = self.client.get(reverse('company-targets'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_aggregated_predictions_view_get(self):
        response = self.client.get(reverse('aggregated_predictions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calculated_hours_view_get(self):
        response = self.client.get(reverse('calculated-hours'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_hours_data_get(self):
        response = self.client.get(reverse('employee-hours-data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
