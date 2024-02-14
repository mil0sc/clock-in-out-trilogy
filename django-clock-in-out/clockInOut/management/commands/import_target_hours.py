from django.core.management.base import BaseCommand
from clockInOut.models import CompanyTarget
import json


class Command(BaseCommand):
    help = 'Exports target hours to a JSON file'

    def handle(self, *args, **options):
        # Fetch target hours
        targets = CompanyTarget.objects.all().values('job_role', 'target_hours')

        # Convert Decimal to str for JSON serialization
        targets_list = [{'job_role': target['job_role'], 'target_hours': str(target['target_hours'])} for target in
                        targets]

        # Define the output path for the JSON file
        output_file_path = 'target_hours.json'
        with open(output_file_path, 'w') as outfile:
            json.dump(targets_list, outfile)

        self.stdout.write(self.style.SUCCESS('Successfully exported target hours to JSON'))
