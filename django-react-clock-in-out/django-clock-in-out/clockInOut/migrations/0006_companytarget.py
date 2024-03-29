# Generated by Django 5.0 on 2024-02-05 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clockInOut', '0005_employee_job_role_alter_timeentry_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_role', models.CharField(max_length=100)),
                ('target_hours', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
