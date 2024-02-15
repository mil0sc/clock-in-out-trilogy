from django.core.management.base import BaseCommand
from clockInOut.models import TimeEntry
import pandas as pd
import math

class Command(BaseCommand):
    help = 'Export TimeEntry data to CSV, including month and calculated work hours.'

    def handle(self, *args, **kwargs):
        entries = TimeEntry.objects.all()
        data = []

        for entry in entries:
            if entry.clock_out and entry.clock_in:
                # Calculate work hours as the difference between clock_out and clock_in in hours
                work_hours = (entry.clock_out - entry.clock_in).total_seconds() / 3600.0
                # Round work hours to the nearest half hour
                work_hours = math.ceil(work_hours * 2) / 2
            else:
                work_hours = 0  # Or handle missing clock_out differently

            data.append({
                'employee_name': entry.employee.name,
                'job_role': entry.employee.job_role,
                'work_category': entry.work_category,
                'work_hours': work_hours,
                'month': entry.clock_in.month
            })

        df = pd.DataFrame(data)
        # Ensure the 'work_hours' column is rounded to one decimal place to represent half hours correctly
        df['work_hours'] = df['work_hours'].round(1)
        df.to_csv('time_entries_data.csv', index=False)
        self.stdout.write(self.style.SUCCESS('Data exported to CSV including month and calculated work hours.'))
