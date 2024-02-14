# aggregate_and_compare.py
from django.core.management.base import BaseCommand
import pandas as pd
from clockInOut.models import TimeEntry, Employee
# Assume 'CompanyTarget' is a model you have that stores target hours for each job role
from clockInOut.models import CompanyTarget


class Command(BaseCommand):
    help = 'Aggregates and compares predicted and actual work hours against company targets.'

    def handle(self, *args, **options):
        # Load actual past hours and predicted future hours into DataFrames
        # This assumes you have a way to distinguish past and future hours, and have already generated 'predictions.json'

        # Example loading data - adjust according to how your data is stored and structured
        actual_past_hours = pd.DataFrame(list(TimeEntry.objects.all().values('employee__job_role', 'work_hours')))
        aggregated_predictions = pd.read_json('predictions.json')
        company_targets = pd.DataFrame(list(CompanyTarget.objects.all().values('job_role', 'target_hours')))

        # Merge, calculate, and compare as detailed in the provided script
        total_yearly_hours = pd.merge(actual_past_hours, aggregated_predictions, on='job_role',
                                      suffixes=('_actual', '_predicted'))
        total_yearly_hours['total_forecasted_hours'] = total_yearly_hours['work_hours_actual'] + total_yearly_hours[
            'work_hours_predicted']
        comparison = pd.merge(total_yearly_hours, company_targets, on='job_role')
        comparison['gap'] = comparison['total_forecasted_hours'] - comparison['target_hours']

        # Output the comparison for review
        print(comparison.to_string())

        # Optionally, save the comparison results to a file or database for further analysis or reporting
