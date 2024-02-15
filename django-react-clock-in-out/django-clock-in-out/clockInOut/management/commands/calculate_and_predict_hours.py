from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Calculates work hours and predictions, then saves to JSON.'

    def handle(self, *args, **options):
        # Your existing script content goes here, slightly adjusted for command use

        # Assuming the CSV and JSON files are located at the root of your Django project
        # You may need to adjust the paths according to your project structure
        csv_file_path = './time_entries_data.csv'
        json_file_path = './target_hours.json'

        try:
            df = pd.read_csv(csv_file_path)

            with open(json_file_path, 'r') as infile:
                target_hours_data = json.load(infile)
                target_hours_dict = {item['job_role']: float(item['target_hours']) for item in target_hours_data}

            current_month = datetime.now().month
            months_passed = current_month - 1

            df_filtered = df[df['month'] <= months_passed]
            total_hours_so_far = df_filtered.groupby('job_role')['work_hours'].sum().reset_index()

            if months_passed > 0:
                predicted_hours_per_month = total_hours_so_far['work_hours'] / months_passed
                total_hours_so_far['predicted_total_hours'] = predicted_hours_per_month * 12

            final_output = [{
                "job_role": row['job_role'],
                "months_passed": months_passed,
                "hours_so_far": row['work_hours'],
                "predicted_total_hours": row.get('predicted_total_hours', 0),
                "target_hours": target_hours_dict.get(row['job_role'], 0)
            } for index, row in total_hours_so_far.iterrows()]

            output_file_path = './calculated_hours.json'
            with open(output_file_path, 'w') as outfile:
                json.dump(final_output, outfile, indent=4)

            self.stdout.write(self.style.SUCCESS('Successfully calculated work hours and predictions.'))

        except Exception as e:
            raise CommandError(f'Error occurred: {str(e)}')
