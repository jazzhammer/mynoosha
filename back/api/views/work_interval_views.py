

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model import Client
from ..model import Project
from ..model.invoice_item import InvoiceItem
from ..model.work_interval import WorkInterval, WorkIntervalSerializer, work_interval_hhmm
from django.utils import timezone
import pytz
timezone.activate(pytz.timezone('UTC'))

from ..model.worker import get_default_worker, Worker
from ..utils.time_utils import utc_ts


def hydrate(adict: dict):
    if adict['stop_utcms']:
        adict['hhmm'] = work_interval_hhmm(adict['start_utcms'], adict['stop_utcms'])
    # greedy populate the invoice_items
    try:
        invoice_item = InvoiceItem.objects.get(pk=adict.invoice_item_id)
        adict['invoice_item'] = model_to_dict(invoice_item)
    except Exception:
        pass
    # greedy populate the projects
    try:
        project = Project.objects.get(pk=adict.project_id)
        adict['project'] = model_to_dict(project)
    except:
        pass
    try:
        adict['start'] = adict['start'].isoformat()
    except:
        pass
    try:
        adict['stop'] = adict['stop'].isoformat()
    except:
        pass

@api_view(['DELETE'])
def work_interval(request, *args, **kwargs):
    if request.method == 'DELETE':
        try:
            deletable = WorkInterval.objects.get(pk=request.data.get('id'))
            deletable.delete()
            return JsonResponse({}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f"{e=}"}, status=404, safe=False)
    else:
        return JsonResponse({'error': f"unhandled request type"}, status=400, safe=False)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def work_intervals(request):
    # expect dt strings for these boundarys:
    pre_start = request.GET.get('pre_start')
    post_start = request.GET.get('post_start')
    pre_stop = request.GET.get('pre_stop')
    post_stop = request.GET.get('post_stop')

    client_id = request.GET.get('client')
    invoice_item = request.GET.get('invoice_item')
    project_id = request.GET.get('project')
    id = request.GET.get('id')
    if request.method == 'GET':
        founds = WorkInterval.objects.all().order_by('start_utcms')
        dt_filtered = False
        if project_id:
            dt_filtered = True
            founds = founds.filter(project_id=project_id)
        if pre_start:
            utcms_from_start = round(utc_ts(iso_format=pre_start))
            founds = founds.filter(start_utcms__gte=utcms_from_start)
            dt_filtered = True
        if post_start:
            utcms_justb4_start = round(utc_ts(iso_format=post_start))
            founds = founds.filter(start_utcms__lt=utcms_justb4_start)
            dt_filtered = True
        if pre_stop:
            utcms_from_stop = round(utc_ts(iso_format=pre_stop))
            founds = founds.filter(stop_utcms__gte=utcms_from_stop)
            dt_filtered = True
        if post_stop:
            utcms_justb4_stop = round(utc_ts(iso_format=post_stop))
            founds = founds.filter(start_utcms__lt=utcms_justb4_stop)
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
                founds = founds.filter(invoice_item_id=invoice_item)
        if dt_filtered:
            # print(founds.query)
            try:
                if not founds.exists() or len(founds) == 0:
                    return JsonResponse([], status=201, safe=False)
                else:
                    dicts = [model_to_dict(instance) for instance in founds]
                    for adict in dicts:
                        hydrate(adict)
                    return JsonResponse(dicts, status=200, safe=False)
            except WorkInterval.DoesNotExist:
                return JsonResponse({'error': f'WorkInterval[{client_id=}] not found'}, status=404, safe=False)
        else:
            founds = WorkInterval.objects.all()
            dicts = [model_to_dict(instance) for instance in founds]
            for adict in dicts:
                adict = hydrate(adict)

            return JsonResponse(dicts, status=200, safe=False)

            # return JsonResponse({'error': f'operation not supported by this set of fields: {request.data}'}, status=400, safe=False)
    if request.method == 'POST':
        # post a stop on all existing unstopped WorkIntervals for the client
        client = request.data['client']
        project = request.data.get('project')
        # get the start string and start ts seconds
        if 'start' in request.data:
            utc_new_s = request.data['start']
        else:
            utc_new_s = timezone.now()
        utc_new_ts = round(utc_ts(iso_format=str(utc_new_s)))

        stoppables = WorkInterval.objects.filter(client=client).filter(stop__isnull=True).order_by('start_utcms')
        for stoppable in stoppables:
            # if the stoppable starts after newWorkInterval's start,
            #   then newWorkInterval's stop is set to the stoppable's start
            if stoppable.start_utcms > utc_new_ts:
                request.data['stop'] = stoppable.start
                request.data['stop_utcms'] = stoppable.start_utcms

            # if the stoppable starts before newWorkInterval's start,
            #   then stoppable's stop is set to the newWorkInterval start
            if utc_new_ts > stoppable.start_utcms:
                stoppable.stop = utc_new_s
                stoppable.stop_utcms = utc_new_ts

            stoppable.save()
        serializer = WorkIntervalSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            if project:
                created.project_id = project
                created.save()
            created = WorkInterval.objects.get(id=created.id)
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
            dict = model_to_dict(created)
            hydrate(dict)
            return JsonResponse(dict, status=201, safe=False)
    if request.method == 'PUT':
        # serializer = WorkIntervalSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=False):
        found = WorkInterval.objects.get(id=request.data['id'])
        if found:
            if request.data.get('stop'):
                found.stop = str(request.data['stop'])
                found.stop_utcms = utc_ts(iso_format=str(request.data['stop']))
                print(f"calculated {found.stop_utcms=} from {request.data['stop']}")
            if request.data.get('description') is None or len(request.data.get('description')) >= 0:
                if request.data.get('description') is None:
                    found.description = ''
                else:
                    found.description = request.data.get('description')
            if request.data.get('invoice_item'):
                invoice_item = InvoiceItem.objects.get(pk=int(request.data.get('invoice_item')))
                found.invoice_item = invoice_item

            if request.data.get('project'):
                project = Project.objects.get(pk=request.data.get('project'))
                found.project = project

            if request.data.get('client'):
                client = Client.objects.get(pk=request.data.get('client'))
                found.client = client

            if request.data.get('worker'):
                worker = Worker.objects.get(pk=request.data.get('worker'))
                found.worker = worker

            found.save()
            updated = found
            dict = model_to_dict(updated)
            hydrate(dict)
            return JsonResponse(dict, status=200, safe=False)
        else:
            return JsonResponse({'error': f"no WorkInterval[{request.data['id']}]"}, status=404, safe=False)

    if request.method == 'DELETE':
        try:
            id = int(request.GET.get('id'))
            WorkInterval.objects.get(id=id).delete()
            return JsonResponse({'detail': f'deleted WorkInterval[{id=}]'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': f'deleted WorkInterval[{e}]'}, status=404)


