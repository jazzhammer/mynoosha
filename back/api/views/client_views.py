from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view

from ..model.client import Client, ClientSerializer
from ..model.agreement import Agreement


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
    name = request.GET.get('name')
    search = request.GET.get('search')
    project = request.GET.get('project')
    founds: QuerySet = Client.objects.all()
    id = request.GET.get('id')
    if id:
        return JsonResponse(model_to_dict(Client.objects.get(pk=id)), status=200, safe=False)
    filtered = False
    if name:
        name = name.strip()
        if len(name) > 0:
            filtered = True
            founds: QuerySet = founds.filter(name=name)

    if search:
        search = search.strip()
        if len(search) > 0:
            filtered = True
            founds: QuerySet = founds.filter(name__contains=search)

    if project:
        filtered = True
        founds: QuerySet = founds.filter(project_id=project)

    if filtered:
        dicts = [model_to_dict(instance) for instance in founds]
        return JsonResponse(dicts, status=200, safe=False)
    else:
        founds = founds.filter()[:10]
        dicts = [model_to_dict(instance) for instance in founds]
        return JsonResponse(dicts, status=200, safe=False)

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
    client = Client.objects.get(pk=id)
    if client:
        # delete dependent agreements
        agreements = Agreement.objects.filter(client_id=id)
        deleted = 0
        for agreement in agreements:
            agreement.delete()
            deleted += 1
        client.delete()
        return JsonResponse({'detail': f'{deleted=}'}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)

@api_view(['GET'])
def clients_count(request: HttpRequest):
    name: str = request.GET.get('name')
    search: str = request.GET.get('search')
    filtered = False
    founds = Client.objects.all()
    if name:
        name = name.strip()
        if len(name) > 0:
            filtered = True
            founds: QuerySet = founds.filter(name=name)
    if search:
        search = search.strip()
        if len(search) > 0:
            filtered = True
            founds: QuerySet = founds.filter(name__contains=search)

    if filtered:
        return JsonResponse(founds.count(), status=200, safe=False)
    else:
        all: QuerySet = Client.objects.all()
        return JsonResponse(all.count(), status=200, safe=False)
