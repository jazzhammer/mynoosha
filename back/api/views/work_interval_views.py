import json
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
    if request.method == 'GET':
        if request.GET.get('id'):
            id = int(request.GET.get('id'))
            try:
                found = WorkInterval.objects.get(pk=id)
                return JsonResponse(model_to_dict(found), status=200)
            except WorkInterval.DoesNotExist:
                return JsonResponse({'error': f'WorkInterval[{id}] not found'}, status=404)
        else:
            pre_start = request.GET.get('pre_start')
            post_start = request.GET.get('post_start')
            pre_stop = request.GET.get('pre_stop')
            post_stop = request.GET.get('post_stop')
            client = request.GET.get('client')
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
                print(founds.query)
                return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
            else:
                return JsonResponse({'error': f'operation not supported by this set of fields: {request.data}'}, status=400, safe=False)
    if request.method == 'POST':
        serializer = WorkIntervalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
    if request.method == 'PUT':
        serializer = WorkIntervalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            updated = serializer.update(WorkInterval.objects.get(pk=request.data['id']), serializer.validated_data)
            return JsonResponse(model_to_dict(updated), status=200, safe=False)
    if request.method == 'DELETE':
        try:
            id = int(request.GET.get('id'))
            WorkInterval.objects.get(id=id).delete()
            return JsonResponse({'detail': f'deleted WorkInterval[{id}]'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': f'deleted WorkInterval[{e}]'}, status=404)