# clockInOut/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

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
