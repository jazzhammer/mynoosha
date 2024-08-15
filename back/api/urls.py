from django.urls import path

from .views.agreement_views import agreements
from .views.client_views import clients
from .views.content_catgory_views import content_categorys
from .views.invoice_item_views import invoice_items
from .views.invoice_views import invoices
from .views.medium_views import mediums
from .views.project_views import projects
from .views.utc_views import utc
from .views.utc_views import utc_iso
from .views.work_interval_views import work_intervals
from .views.work_interval_views import work_interval
from .views.work_piece_views import work_pieces
from .views.work_type_views import work_types
from .views.billable_type_views import billable_types
from .views.client_billable_type_views import client_billable_types
from .views.worker_views import workers

urlpatterns = [
    path('agreements/', agreements),
    path('billable_types/', billable_types),
    path('clients/', clients),
    path('client_billable_types/', client_billable_types),
    path('content_categorys/', content_categorys),
    path('invoices/', invoices),
    path('invoice_items/', invoice_items),
    path('mediums/', mediums),
    path('projects/', projects),
    path('workers/', workers),
    path('work_interval/', work_interval),
    path('work_intervals/', work_intervals),
    path('work_pieces/', work_pieces),
    path('work_types/', work_types),
    path('utc/', utc),
    path('utc/iso', utc_iso)
]

