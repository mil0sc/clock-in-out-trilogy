from django.core.management.base import BaseCommand
import pandas as pd
import json

class Command(BaseCommand):
    help = 'Sums and sorts employee hours from a CSV file, exports to JSON including job roles.'

    def handle(self, *args, **options):
        df = pd.read_csv('time_entries_data.csv')

        # Group by both employee_name and job_role, then sum hours and round
        grouped = df.groupby(['employee_name', 'job_role'])['work_hours'].sum().round(0).reset_index()

        # Sort the DataFrame by total_hours in descending order
        sorted_grouped = grouped.sort_values(by='work_hours', ascending=False)

        # Convert to list of dictionaries for JSON
        employees_hours_list = sorted_grouped.to_dict('records')

        # Define the JSON output file path
        output_file_path = 'sorted_employee_hours_with_roles.json'

        # Export to JSON
        with open(output_file_path, 'w') as outfile:
            json.dump(employees_hours_list, outfile, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported sorted employee hours with roles to {output_file_path}.'))
