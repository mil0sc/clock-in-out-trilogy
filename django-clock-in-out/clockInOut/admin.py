from django.contrib import admin
from django.http import HttpResponse
from .models import Employee, TimeEntry, CompanyTarget
from django import forms
import csv


class TimeEntryInline(admin.TabularInline):
    model = TimeEntry
    extra = 0


class ShiftHoursFilter(admin.SimpleListFilter):
    title = 'shift hours'
    parameter_name = 'shift_hours'

    def lookups(self, request, model_admin):
        return [
            ('6-14', 'Morning Shift (6-14)'),
            ('14-22', 'Evening Shift (14-22)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '6-14':
            return queryset.filter(shift_hours='6-14')
        elif self.value() == '14-22':
            return queryset.filter(shift_hours='14-22')
        return queryset


def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


export_as_csv.short_description = "Export Selected as CSV"


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'  # This already includes the job_role field
        help_texts = {
            'shift_hours': 'Please enter shift hours in the format "6-14" for Morning Shift or "14-22" for Evening Shift.',
            'job_role': 'Please select the job role for the employee.',  # Add help text for job_role if desired
        }
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm  # Continue using the custom form for Employee
    list_display = ('name', 'shift_hours', 'job_role')  # Add 'job_role' to the fields displayed in the list
    search_fields = ('name',)
    inlines = [TimeEntryInline]
    list_filter = (ShiftHoursFilter, 'job_role')  # Add 'job_role' to filters
    actions = [export_as_csv]

class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'clock_in', 'clock_out', 'work_category')
    list_filter = ('employee', 'work_category')
    search_fields = ('employee__name',)
class CompanyTargetAdmin(admin.ModelAdmin):
    list_display = ('job_role', 'target_hours')
    search_fields = ('job_role',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(TimeEntry, TimeEntryAdmin)
admin.site.register(CompanyTarget, CompanyTargetAdmin)