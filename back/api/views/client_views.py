
from django.forms import model_to_dict
from django.http import JsonResponse
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
    if request.GET.get('search'):
        search = request.GET.get('search')
        founds = Client.objects.filter(name__contains=search)
        if founds.exists():
            dicts = [model_to_dict(instance) for instance in founds]
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse(
                {'detail': f'empty result for search={search}'},
                status=201,
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
