from django.contrib import admin
from django.urls import include, path
from clockInOut import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clockinout/', include('clockInOut.urls')),
    path('clock-in-out/', views.clock_in_out_view, name='clock_in_out'),
    path('calculate-hours/', views.work_hours_view, name='calculate_hours'),
    path('generate-report/', views.generate_report_view, name='generate_report'),
    path('employees/', views.employee_list_view, name='employee-list'),
    path('time-entries/', views.time_entries_list_view, name='time-entries-list'),
    path('', views.main_dashboard, name='main-dashboard'),
    path('api/employees/', views.EmployeeList.as_view(), name='employee-list'),
    path('api/time-entries/', views.TimeEntryList.as_view(), name='time-entry-list'),
    path('api/predictions/', views.predictions_view, name='predictions'),
    path('api/aggregated-predictions/', views.aggregated_predictions_api, name='aggregated_predictions_api'),
    path('api/company-targets/', views.company_targets_view, name='company-targets'),
    path('api/year-predictions/', views.aggregated_predictions_view, name='aggregated_predictions'),
    path('api/year-predicted/', views.combined_data_view, name='views'),
    path('api/calculated-hours/', views.calculated_hours_view, name='calculated-hours'),
    path('api/employee-hours/', views.employee_hours_data, name='employee-hours-data'),
]
