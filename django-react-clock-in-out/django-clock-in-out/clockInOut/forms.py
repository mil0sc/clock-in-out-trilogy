# forms.py
from django import forms


class ClockInOutForm(forms.Form):
    employee_id = forms.IntegerField(label='Employee ID', min_value=1)
    action = forms.ChoiceField(choices=[('IN', 'Clock In'), ('OUT', 'Clock Out')])
    # Adding work category choice here
    work_category = forms.ChoiceField(choices=[('Remote', 'Remote'), ('Stationary', 'Stationary')], label='Work '
                                                                                                          'Category')


class WorkHoursForm(forms.Form):
    employee_id = forms.IntegerField(label='Employee ID', min_value=1)


class ReportForm(forms.Form):
    employee_id = forms.IntegerField(label='Employee ID (optional)', required=False, min_value=1)
