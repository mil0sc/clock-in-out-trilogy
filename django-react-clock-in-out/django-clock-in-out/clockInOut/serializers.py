# serializers.py
from rest_framework import serializers
from .models import Employee, TimeEntry

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    time_entries = TimeEntrySerializer(many=True, read_only=True)  # Add this line

    class Meta:
        model = Employee
        fields = '__all__'  # Ensure this includes the nested time_entries
