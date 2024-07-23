import json
import math
from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..models import Client, WorkInterval
from ..serializers import ClientSerializer, WorkIntervalSerializer
from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('UTC'))



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def work_intervals(request):
    pre_start = request.GET.get('pre_start')
    post_start = request.GET.get('post_start')
    pre_stop = request.GET.get('pre_stop')
    post_stop = request.GET.get('post_stop')
    client = request.GET.get('client')
    if request.method == 'GET':
        if request.GET.get('id'):
            id = int(request.GET.get('id'))
            try:
                found = WorkInterval.objects.get(pk=id)
                return JsonResponse(model_to_dict(found), status=200)
            except WorkInterval.DoesNotExist:
                return JsonResponse({'error': f'WorkInterval[{id}] not found'}, status=404)
        else:
            founds = WorkInterval.objects.all()
            dt_filtered = False
            if pre_start:
                utcms_from_start = round(datetime.fromisoformat(pre_start).timestamp())
                founds = founds.filter(start_utcms__gte=utcms_from_start)
                dt_filtered = True
            if post_start:
                utcms_justb4_start = round(datetime.fromisoformat(post_start).timestamp())
                founds = founds.filter(start_utcms__lt=utcms_justb4_start)
                dt_filtered = True
            if pre_stop:
                utcms_from_stop = round(datetime.fromisoformat(pre_stop).timestamp())
                founds = WorkInterval.objects.filter(stop_utcms__gte=utcms_from_stop)
                dt_filtered = True
            if post_stop:
                utcms_justb4_stop = round(datetime.fromisoformat(post_stop).time())
                founds = founds.filter(start_utcms__lt=utcms_justb4_stop)
                dt_filtered = True
            if client:
                founds = founds.filter(client=client)
                dt_filtered = True
            if dt_filtered:
                # print(founds.query)
                dicts = [model_to_dict(instance) for instance in founds]
                for adict in dicts:
                    if adict['stop_utcms']:
                        stop = adict['stop_utcms']
                        start = adict['start_utcms']
                        diff = stop - start  # seconds
                        if diff < 3600:
                            HH = 0
                        else:
                            HH = math.floor(diff / 3600)
                        MM = math.floor((diff % 3600) / 60)
                        hhstr = f'{HH}' if HH > 9 else f'0{HH}'
                        mmstr = f'{MM}' if MM > 9 else f'0{MM}'
                        hhmm = f'{hhstr}:{mmstr}'
                        print(f"composed {hhmm}")
                        adict['hhmm'] = hhmm
                return JsonResponse(dicts, status=200, safe=False)
                # dicts = [model_to_dict(instance) for instance in founds]
                # serializers = [WorkIntervalSerializer(data=dict) for dict in dicts]
                # json_array = []
                # for serializer in serializers:
                #     serializer.is_valid(raise_exception=True)
                #     print(serializer.data)
                #     json_array.append(serializer.data)
                # # return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
                # return JsonResponse(json_array, status=200, safe=False)
            else:
                return JsonResponse({'error': f'operation not supported by this set of fields: {request.data}'}, status=400, safe=False)
    if request.method == 'POST':
        #post a stop on all existing unstopped WorkIntervals for the client
        client = request.data['client']
        stoppables = WorkInterval.objects.filter(client=client).filter(stop__isnull=True)
        utc_now = timezone.now()

        utc_now_ts = utc_now.timestamp()
        utc_now_s = str(utc_now)
        for stoppable in stoppables:
            stoppable.stop = utc_now_s
            stoppable.stop_utcms = utc_now_ts
            stoppable.save()
        serializer = WorkIntervalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
    if request.method == 'PUT':
        # serializer = WorkIntervalSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=False):
        found = WorkInterval.objects.get(id=request.data['id'])
        if found:
            if request.data.get('stop'):
                stops = str(request.data['stop'])
                if stops.endswith('Z'):
                    stops = stops[:-1]
                    found.stop = stops

                    utc_stop = timezone.datetime.fromisoformat(stops)
                    found.stop_utcms = utc_stop.timestamp()

            if len(request.data.get('description')) >= 0:
                next_description = request.data.get('description')
                found.description = next_description

            found.save()
            updated = found
            return JsonResponse(model_to_dict(updated), status=200, safe=False)
        else:
            return JsonResponse({'error': f"no WorkInterval[{request.data['id']}]"}, status=404, safe=False)

    if request.method == 'DELETE':
        try:
            id = int(request.GET.get('id'))
            WorkInterval.objects.get(id=id).delete()
            return JsonResponse({'detail': f'deleted WorkInterval[{id}]'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': f'deleted WorkInterval[{e}]'}, status=404)