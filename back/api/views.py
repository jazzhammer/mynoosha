import json

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Client, WorkInterval
from .serializers import ClientSerializer, WorkIntervalSerializer


@api_view(['GET', 'POST', 'DELETE'])
def clients(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            search = request.GET.get('search')
            founds = Client.objects.filter(name__contains=search)
            if founds.exists():
                return JsonResponse(json.dumps([model_to_dict(instance) for instance in founds]), status=200, safe=False)
            else:
                return JsonResponse(
                    json.dumps({'detail':f'empty result for search={search}'}),
                    status=404,
                    safe=False
                )
        else:
            return JsonResponse(
                json.dumps([model_to_dict(instance) for instance in Client.objects.all().order_by('name')]),
                status=200,
                safe=False)
    elif request.method == 'POST':
        if not Client.objects.filter(name=request.GET.get('name')).exists():
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                created = serializer.save()
                return JsonResponse(model_to_dict(created), status=201, safe=False)
            else:
                return JsonResponse({'error': 'invalid data for Client'}, status=400, safe=False)
        else:
            return JsonResponse({'error': 'Client already exists'}, status=400, safe=False)
    elif request.method == 'DELETE':
        id = request.GET.get('id')
        if Client.objects.filter(id=id).exists():
            Client.objects.filter(id=id).delete()
            return JsonResponse({}, status=200, safe=False)
        else:
            return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
    else:
        return JsonResponse(json.dumps({'data': f"{request.method} unsupported"}), status=400, safe=False)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def work_intervals(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        serializer = WorkIntervalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        try:
            id = int(request.GET.get('id'))
            WorkInterval.objects.get(id=id).delete()
            return JsonResponse({'detail': f'deleted WorkInterval[{id}]'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': f'deleted WorkInterval[{e}]'}, status=404)