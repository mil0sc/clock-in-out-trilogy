from django.urls import path
from . import views

urlpatterns = [
    path('your-view/', views.your_view, name='your_view'),
]
