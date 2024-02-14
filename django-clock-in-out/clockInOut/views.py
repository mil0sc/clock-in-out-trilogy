# views.py

from rest_framework import generics
from django.shortcuts import render
from django.conf import settings
import os
from .forms import ClockInOutForm, WorkHoursForm, ReportForm
from .models import Employee, TimeEntry, CompanyTarget
from .utils import calculate_hours, clock_in_employee, clock_out_employee
from .serializers import EmployeeSerializer, TimeEntrySerializer
from django.http import JsonResponse
import json



def your_view(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        # Process the data...
        return render(request, 'your_template.html', {'submitted': True, 'employee_id': employee_id})

    return render(request, 'your_template.html', {'submitted': False})


def employee_list_view(request):
    employees = Employee.objects.all()  # Retrieve all employees
    return render(request, 'employee_list.html', {'employees': employees})


def time_entries_list_view(request):
    time_entries = TimeEntry.objects.all().select_related(
        'employee')  # Retrieve all time entries with related employee data
    return render(request, 'time_entries_list.html', {'time_entries': time_entries})


'''
def some_employee_view(request, employee_id):
    hours = calculate_hours(employee_id)
    return render(request, 'some_template.html', {'hours': hours})
'''


def clock_in_out_view(request):
    if request.method == 'POST':
        form = ClockInOutForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            action = form.cleaned_data['action']
            work_category = form.cleaned_data['work_category']  # Capture work category from form

            # Assume clock_in_employee and clock_out_employee are modified to accept work_category
            if action == 'IN':
                status, message = clock_in_employee(employee_id, work_category)
            else:
                status, message = clock_out_employee(employee_id)

            return render(request, 'clock_in_out_result.html', {'status': status, 'message': message})
    else:
        form = ClockInOutForm()

    return render(request, 'clock_in_out_form.html', {'form': form})


def work_hours_view(request):
    if request.method == 'POST':
        form = WorkHoursForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            hours = calculate_hours(employee_id)
            return render(request, 'work_hours_report.html', {'hours': hours, 'employee_id': employee_id})
    else:
        form = WorkHoursForm()

    return render(request, 'work_hours_form.html', {'form': form})


def generate_report_view(request):
    form = ReportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        employee_id = form.cleaned_data.get('employee_id')
        if employee_id:
            entries = TimeEntry.objects.filter(employee_id=employee_id).select_related('employee')
        else:
            entries = TimeEntry.objects.all().select_related('employee')

        report_data = [
            {
                "employee_name": entry.employee.name,
                "timestamp": entry.clock_in,
                "action": "Clock In" if entry.clock_out is None else "Clock Out"
            }
            for entry in entries
        ]

        return render(request, 'report_result.html', {'report_data': report_data})

    # This return will handle both GET requests and POST requests where the form is not valid
    return render(request, 'report_form.html', {'form': form})


class TimeEntryList(generics.ListAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer


class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


def main_dashboard(request):
    return render(request, 'main_dashboard.html')

def predictions_view(request):
    with open('predictions.json', 'r') as file:
        predictions = json.load(file)
    return JsonResponse(predictions, safe=False)

def aggregated_predictions_api(request):
    try:
        with open('aggregated_predictions.json', 'r') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False)
    except FileNotFoundError:
        return JsonResponse({'error': 'Aggregated predictions not found.'}, status=404)


def company_targets_view(request):
    # Fetch all company targets from the database
    targets = CompanyTarget.objects.all().values('job_role', 'target_hours')

    # Convert QuerySet to a list to make it JSON serializable
    targets_list = list(targets)

    # Return the targets as JSON
    return JsonResponse(targets_list, safe=False)

def aggregated_predictions_view(request):
    # Define the path to the JSON file using settings.BASE_DIR for portability across environments
    file_path = os.path.join(settings.BASE_DIR, 'calculated_hours.json')

    # Open the JSON file and load its content
    with open(file_path, 'r') as file:
        predictions = json.load(file)

    # Return the predictions as JSON
    return JsonResponse(predictions, safe=False)


def combined_data_view(request):
    # Assuming you have a function to get worked and predicted hours
    worked_and_predicted_hours = get_worked_and_predicted_hours()  # Implement this

    # Fetch target hours from database
    targets = CompanyTarget.objects.all().values('job_role', 'target_hours')
    target_hours_dict = {target['job_role']: target['target_hours'] for target in targets}

    # Combine data
    for entry in worked_and_predicted_hours:
        job_role = entry['job_role']
        entry['target_hours'] = target_hours_dict.get(job_role, '0.00')

    # Return combined data as JSON
    return JsonResponse(worked_and_predicted_hours, safe=False)

def calculated_hours_view(request):
    # Construct the full path to the json file
    file_path = os.path.join(settings.BASE_DIR, 'calculated_hours.json')

    # Open and read the json file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Return the data as JSON
    return JsonResponse(data, safe=False)  # safe=False is required for non-dict objects


def employee_hours_data(request):
    # Path to the JSON file generated by the management command
    file_path = 'sorted_employee_hours_with_roles.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    return JsonResponse(data, safe=False)  # safe=False is necessary for non-dict objects