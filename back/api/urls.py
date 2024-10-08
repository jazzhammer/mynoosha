from django.urls import path

from .views.agreement_views import agreements, agreements_count
from .views.client_views import clients, clients_count
from .views.content_catgory_views import content_categorys
from .views.invoice_item_views import invoice_items
from .views.invoice_views import invoices
from .views.medium_views import mediums
from .views.project_views import projects, projects_count
from .views.project_type_views import project_types
from .views.utc_views import utc
from .views.utc_views import utc_iso
from .views.work_interval_views import work_intervals
from .views.work_interval_views import work_interval
from .views.work_milestone_views import work_milestones
from .views.work_piece_views import work_pieces
from .views.work_type_views import work_types
from .views.billable_type_views import billable_types
from .views.client_billable_type_views import client_billable_types
from .views.worker_rate_views import worker_rates
from .views.worker_views import workers

urlpatterns = [
    path('agreements/', agreements),
    path('agreements/count', agreements_count),
    path('billable_types/', billable_types),
    path('clients/', clients),
    path('clients/count', clients_count),
    path('client_billable_types/', client_billable_types),
    path('content_categorys/', content_categorys),
    path('invoices/', invoices),
    path('invoice_items/', invoice_items),
    path('mediums/', mediums),
    path('projects/', projects),
    path('projects/count', projects_count),
    path('project_types/', project_types),
    path('workers/', workers),
    path('work_interval/', work_interval),
    path('work_intervals/', work_intervals),
    path('work_pieces/', work_pieces),
    path('work_milestones/', work_milestones),
    path('work_types/', work_types),
    path('worker_rates/', worker_rates),
    path('utc/', utc),
    path('utc/iso', utc_iso)
]

