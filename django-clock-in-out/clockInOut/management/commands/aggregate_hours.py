# aggregate_hours.py
from django.core.management.base import BaseCommand
from django.db.models import Sum
from clockInOut.models import TimeEntry
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Aggregate work hours by job role and month.'

    def handle(self, *args, **kwargs):
        current_year = datetime.now().year
        entries = TimeEntry.objects.filter(clock_in__year=current_year)
        data = entries.values('employee__job_role', 'clock_in__month').annotate(total_hours=Sum('work_hours'))
        df = pd.DataFrame(list(data))

        print(df)  # or save to CSV, JSON, etc.
