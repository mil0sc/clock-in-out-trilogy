from django.db import models

# Define JOB_ROLES at the module level so it's accessible to all classes
JOB_ROLES = [
    ('frontend', 'Frontend Developer'),
    ('backend', 'Backend Developer'),
    ('devops', 'DevOps Engineer'),
    ('datasci', 'Data Scientist'),
    ('projmgr', 'Project Manager'),
]

class Employee(models.Model):
    SHIFT_CHOICES = [
        ('6-14', 'Morning Shift (6-14)'),
        ('14-22', 'Evening Shift (14-22)'),
        # Add more predefined shifts as needed
    ]
    name = models.CharField(max_length=100)
    shift_hours = models.CharField(max_length=50, choices=SHIFT_CHOICES)
    job_role = models.CharField(max_length=20, choices=JOB_ROLES, default='backend')  # Use JOB_ROLES here

class TimeEntry(models.Model):
    REMOTE = 'Remote'
    STATIONARY = 'Stationary'
    WORK_CATEGORY_CHOICES = [
        (REMOTE, 'Remote'),
        (STATIONARY, 'Stationary'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='time_entries')
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    work_category = models.CharField(max_length=10, choices=WORK_CATEGORY_CHOICES, default=STATIONARY)

class CompanyTarget(models.Model):
    job_role = models.CharField(max_length=20, choices=JOB_ROLES)  # Now JOB_ROLES is accessible here
    target_hours = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_job_role_display()}: {self.target_hours} hours target"
