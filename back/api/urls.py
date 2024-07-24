from django.urls import path

from .views.client_views import clients
from .views.work_interval_views import work_intervals
from .views.work_interval_views import work_interval

urlpatterns = [
    path('clients/', clients),
    path('work_intervals/', work_intervals),
    path('work_interval/', work_interval),
]