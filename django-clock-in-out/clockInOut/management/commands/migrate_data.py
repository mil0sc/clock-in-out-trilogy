from django.core.management.base import BaseCommand
import sqlite3
from ...models import Employee, TimeEntry  # Correct path to your models
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = 'Migrates data from the old SQLite database to the new Django database'

    def add_arguments(self, parser):
        parser.add_argument('sqlite_db_path', type=str, help='Path to your old SQLite database')

    def handle(self, *args, **options):
        sqlite_db_path = options['sqlite_db_path']
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()

        # Migrate employees
        cursor.execute("SELECT id, name, shift_hours FROM employees")
        for row in cursor.fetchall():
            Employee.objects.create(id=row[0], name=row[1], shift_hours=row[2])

        # Migrate time entries
        cursor.execute("SELECT employee_id, timestamp, action FROM time_entries")
        for employee_id, timestamp, action in cursor.fetchall():
            employee = Employee.objects.get(id=employee_id)
            timestamp = parse_datetime(timestamp)
            # Logic for 'IN' and 'OUT' actions
            if action == 'IN':
                TimeEntry.objects.create(employee=employee, clock_in=timestamp)
            elif action == 'OUT':
                time_entry = TimeEntry.objects.filter(employee=employee, clock_in__lte=timestamp).last()
                if time_entry:
                    time_entry.clock_out = timestamp
                    time_entry.save()

        conn.close()
        self.stdout.write(self.style.SUCCESS('Successfully migrated data from SQLite to Django'))
