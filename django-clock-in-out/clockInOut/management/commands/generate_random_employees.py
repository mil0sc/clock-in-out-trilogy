from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from clockInOut.models import Employee, TimeEntry

class Command(BaseCommand):
    help = 'Generates random employees with clock-in/out data for the past 3 months.'

    def handle(self, *args, **options):
        job_roles = ['frontend', 'backend', 'devops', 'datasci', 'projmgr']
        shift_choices = ['6-14', '14-22']

        # Generate 50 random employees
        for i in range(50):
            employee = Employee.objects.create(
                name=f'Employee {i}',
                shift_hours=random.choice(shift_choices),
                job_role=random.choice(job_roles)
            )

            # Generate clock-in/out data for the past 90 days
            for day in range(90):
                # Randomly decide whether to skip clocking in/out for this day
                if random.randint(1, 20) != 1:  # On average, skips once every 20 days
                    clock_in_time = timezone.now() - timedelta(days=day, hours=random.randint(6, 9))
                    work_duration = random.uniform(4, 8)
                    clock_out_time = clock_in_time + timedelta(hours=work_duration)

                    TimeEntry.objects.create(
                        employee=employee,
                        clock_in=clock_in_time,
                        clock_out=clock_out_time,
                        work_category=random.choice(['Remote', 'Stationary'])
                    )

        self.stdout.write(self.style.SUCCESS('Successfully generated random employees and time entries.'))
