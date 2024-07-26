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


@api_view(['GET', 'POST', 'DELETE'])
def clients(request, *args, **kwargs):
    if request.method == 'GET':
        return get_clients(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_clients(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_clients(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_clients(request, *args, **kwargs):
    if request.GET.get('search'):
        search = request.GET.get('search')
        founds = Client.objects.filter(name__contains=search)
        if founds.exists():
            dicts = [model_to_dict(instance) for instance in founds]
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse(
                {'detail': f'empty result for search={search}'},
                status=404,
                safe=False
            )
    else:
        return JsonResponse(
            [model_to_dict(instance) for instance in Client.objects.all().order_by('name')],
            status=200,
            safe=False)


def post_clients(request, *args, **kwargs):
    if not Client.objects.filter(name=request.GET.get('name')).exists():
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
        else:
            return JsonResponse({'error': 'invalid data for Client'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'Client already exists'}, status=400, safe=False)

def delete_clients(request, *args, **kwargs):
    id = request.GET.get('id')
    if Client.objects.filter(id=id).exists():
        Client.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
