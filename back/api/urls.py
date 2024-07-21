from django.urls import path

from .views import clients, work_intervals

urlpatterns = [
    path('clients/', clients),
    path('work_intervals/', work_intervals),
]