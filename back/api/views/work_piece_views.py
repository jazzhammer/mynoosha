from datetime import datetime

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model.client import Client
from ..model.invoice_item import InvoiceItem
from ..model.work_piece import WorkPiece, WorkPieceSerializer
from django.utils import timezone
import pytz
timezone.activate(pytz.timezone('UTC'))

from ..model.worker import get_default_worker, Worker


@api_view(['DELETE'])
def work_piece(request, *args, **kwargs):
    if request.method == 'DELETE':
        try:
            deletable = WorkPiece.objects.get(pk=request.data.get('id'))
            deletable.delete()
            return JsonResponse({}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f"{e=}"}, status=404, safe=False)
    else:
        return JsonResponse({'error': f"unhandled request type"}, status=400, safe=False)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def work_pieces(request):
    # expect dt strings for these boundarys:
    pre_start = request.GET.get('pre_start')
    post_start = request.GET.get('post_start')

    client_id = request.GET.get('client')
    invoice_item = request.GET.get('invoice_item')
    project = request.GET.get('project')

    id = request.GET.get('id')
    if request.method == 'GET':
        founds: QuerySet = WorkPiece.objects.all().order_by('start')
        filtered = False
        if pre_start:
            from_start = datetime.fromisoformat(pre_start)
            founds = founds.filter(start__gte=from_start)
            filtered = True
        if post_start:
            justb4_start = datetime.fromisoformat(post_start)
            founds = founds.filter(start__lt=justb4_start)
            filtered = True
        if client_id:
            try:
                int(client_id)
            except ValueError:
                return JsonResponse({'error': f"invalid {client_id=}"}, status=400)
            founds = founds.filter(client=client_id)
            filtered = True
        if id:
            try:
                int(id)
            except ValueError:
                return JsonResponse({'error': f"invalid {id=}"}, status=400)
            founds = founds.filter(id=id)
            filtered = True
        if invoice_item:
            filtered = True
            if invoice_item == 'isnull':
                founds = founds.filter(invoice_item__isnull=True)
            else:
                founds = founds.filter(invoice_item=invoice_item)
        if project:
            filtered = True
            founds = founds.filter(project_id=project)
        if filtered:
            if not founds.exists() or len(founds) == 0:
                return JsonResponse([], status=201, safe=False)
            else:
                dicts = [model_to_dict(instance) for instance in founds]
                return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse({'error': f'operation not supported by this set of fields: {request.data}'}, status=400, safe=False)
    if request.method == 'POST':
        serializer = WorkPieceSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            created = WorkPiece.objects.get(id=created.id)
            # automate the worker assignment for this new workInterval if not provided
            worker = None
            try:
                worker = Worker.objects.get(id=request.data.get('worker'))
            except Exception as e:
                print(f"no worker for {request.data.get('worker')=}")
            if worker is None:
                default_worker = get_default_worker()
                created.worker = default_worker
            else:
                created.worker = worker
            created.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
    if request.method == 'PUT':
        # serializer = WorkPieceSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=False):
        found = WorkPiece.objects.get(id=request.data['id'])
        if found:
            if request.data.get('description') is not None or len(request.data.get('description')) >= 0:
                found.description = request.data.get('description')
            if request.data.get('name') is not None or len(request.data.get('name')) >= 0:
                found.name = request.data.get('name')
            if request.data.get('client') is not None or len(request.data.get('client')) >= 0:
                found.client = Client.objects.get(pk=request.data.get('client'))
            if request.data.get('invoice_item'):
                invoice_item = InvoiceItem.objects.get(pk=int(request.data.get('invoice_item')))
                found.invoice_item = invoice_item

            found.save()
            updated = found
            return JsonResponse(model_to_dict(updated), status=200, safe=False)
        else:
            return JsonResponse({'error': f"no WorkPiece[{request.data['id']}]"}, status=404, safe=False)

    if request.method == 'DELETE':
        try:
            id = int(request.GET.get('id'))
            WorkPiece.objects.get(id=id).delete()
            return JsonResponse({'detail': f'deleted WorkPiece[{id=}]'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': f'deleted WorkPiece[{e}]'}, status=404)

