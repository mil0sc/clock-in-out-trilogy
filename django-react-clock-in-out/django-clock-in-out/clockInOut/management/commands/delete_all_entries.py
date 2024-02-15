from django.core.management.base import BaseCommand
from clockInOut.models import Employee, TimeEntry, CompanyTarget

class Command(BaseCommand):
    help = 'Deletes all entries from Employee, TimeEntry, and CompanyTarget models.'

    def handle(self, *args, **options):
        # Confirm before deleting
        if input("Are you sure you want to delete all entries? This cannot be undone. Type 'yes' to continue: ") != 'yes':
            self.stdout.write(self.style.WARNING('Operation canceled.'))
            return

        # Deleting entries
        Employee.objects.all().delete()
        TimeEntry.objects.all().delete()
        CompanyTarget.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all entries from Employee, TimeEntry, and CompanyTarget models.'))
