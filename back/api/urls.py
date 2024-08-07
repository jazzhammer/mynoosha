from django.urls import path

from .views.agreement_views import agreements
from .views.client_views import clients
from .views.invoice_views import invoices
from .views.project_views import projects
from .views.work_interval_views import work_intervals
from .views.work_interval_views import work_interval
from .views.work_type_views import work_types
from .views.billable_type_views import billable_types
from .views.client_billable_type_views import client_billable_types

urlpatterns = [
    path('agreements/', agreements),
    path('billable_types/', billable_types),
    path('clients/', clients),
    path('client_billable_types/', client_billable_types),
    path('invoices/', invoices),
    path('projects/', projects),
    path('work_interval/', work_interval),
    path('work_intervals/', work_intervals),
    path('work_types/', work_types),
]

