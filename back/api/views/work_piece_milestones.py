from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model.client import Client
from ..model.invoice_item import InvoiceItem
from ..model.work_milestone import WorkMilestone, WorkMilestoneSerializer
from django.utils import timezone
import pytz
timezone.activate(pytz.timezone('UTC'))

from ..model.worker import get_default_worker, Worker
from ..utils.time_utils import utc_ts


@api_view(['DELETE'])
def work_milestone(request, *args, **kwargs):
    if request.method == 'DELETE':
        try:
            deletable = WorkMilestone.objects.get(pk=request.data.get('id'))
            deletable.delete()
            return JsonResponse({}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f"{e=}"}, status=404, safe=False)
    else:
        return JsonResponse({'error': f"unhandled request type"}, status=400, safe=False)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def work_milestones(request):
    # expect dt strings for these boundarys:
    pre_start = request.GET.get('pre_start')
    post_start = request.GET.get('post_start')

    client_id = request.GET.get('client')
    invoice_item = request.GET.get('invoice_item')

    id = request.GET.get('id')
    if request.method == 'GET':
        founds = WorkMilestone.objects.all().order_by('start_utcms')
        dt_filtered = False
        if pre_start:
            utcms_from_start = round(utc_ts(iso_format=pre_start))
            founds = founds.filter(start_utcms__gte=utcms_from_start)
            dt_filtered = True
        if post_start:
            utcms_justb4_start = round(utc_ts(iso_format=post_start))
            founds = founds.filter(start_utcms__lt=utcms_justb4_start)
            dt_filtered = True
        if client_id:
            try:
                int(client_id)
            except ValueError:
                return JsonResponse({'error': f"invalid {client_id=}"}, status=400)
            founds = founds.filter(client=client_id)
            dt_filtered = True
        if id:
            try:
                int(id)
            except ValueError:
                return JsonResponse({'error': f"invalid {id=}"}, status=400)
            founds = founds.filter(id=id)
            dt_filtered = True
        if invoice_item:
            if invoice_item == 'isnull':
                founds = founds.filter(invoice_item__isnull=True)
            else:
                founds = founds.filter(invoice_item=invoice_item)
        if dt_filtered:
            # print(founds.query)
            try:
                if not founds.exists() or len(founds) == 0:
                    return JsonResponse([], status=201, safe=False)
                else:
                    dicts = [model_to_dict(instance) for instance in founds]
                    return JsonResponse(dicts, status=200, safe=False)
            except WorkMilestone.DoesNotExist:
                return JsonResponse({'error': f'WorkMilestone[{client_id=}] not found'}, status=404, safe=False)
        else:
            return JsonResponse({'error': f'operation not supported by this set of fields: {request.data}'}, status=400, safe=False)
    if request.method == 'POST':
        serializer = WorkMilestoneSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            created = WorkMilestone.objects.get(id=created.id)
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
        # serializer = WorkMilestoneSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=False):
        found = WorkMilestone.objects.get(id=request.data['id'])
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
            return JsonResponse({'error': f"no WorkMilestone[{request.data['id']}]"}, status=404, safe=False)

    if request.method == 'DELETE':
        try:
            id = int(request.GET.get('id'))
            WorkMilestone.objects.get(id=id).delete()
            return JsonResponse({'detail': f'deleted WorkMilestone[{id=}]'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': f'deleted WorkMilestone[{e}]'}, status=404)

