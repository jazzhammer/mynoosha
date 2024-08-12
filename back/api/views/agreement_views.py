from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model.agreement import Agreement, AgreementSerializer
from ..model.client import Client
from ..model.worker import Worker


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def agreements(request, *args, **kwargs):
    if request.method == 'GET':
        return get_agreements(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_agreements(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_agreements(request, *args, **kwargs)
    elif request.method == 'PUT':
        return put_agreements(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_agreements(request, *args, **kwargs):
    client = request.GET.get('client')
    worker = request.GET.get('worker')
    name = request.GET.get('name')
    type = request.GET.get('type')
    founds = Agreement.objects.all()
    filtered = False
    if name:
        filtered = True
        founds = founds.filter(name__contains=name)
    if client:
        filtered = True
        founds = founds.filter(client_id=client)
    if worker:
        filtered = True
        founds = founds.filter(worker_id=worker)
    if type:
        filtered = True
        founds = founds.filter(type=type)

    if filtered:
        if founds.exists():
            dicts = [model_to_dict(instance) for instance in founds]
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)
    else:
        return JsonResponse(
            {'detail': f'empty result for search parameters {client=}, {worker=}, {type=}, {name=}'},
            status=200,
            safe=False
        )

def post_agreements(request, *args, **kwargs):
    if not Agreement.objects.filter(name=request.GET.get('name')).exists():
        serializer = AgreementSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
        else:
            return JsonResponse({'error': 'invalid data for Agreement'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'Agreement already exists'}, status=400, safe=False)

def put_agreements(request, *args, **kwargs):
    id = request.data.get('id')
    if not id:
        return JsonResponse({'error': f'no agreement for missing {id=}'}, status=400, safe=False)
    try:
        agreement = Agreement.objects.get(pk=id)
    except Exception:
        return JsonResponse({'error': f'no agreement for {id=}'}, status=400, safe=False)

    if agreement:
        name = request.data.get('name')
        client = request.data.get('client')
        worker = request.data.get('worker')
        type = request.data.get('type')
        if name:
            agreement.name = name
        if client:
            agreement.client = Client.objects.get(pk=client)
        if worker:
            agreement.worker = Worker.objects.get(pk=worker)
        if type:
            agreement.type = type
        agreement.save()
        return JsonResponse(model_to_dict(agreement), status=200, safe=False)
    else:
        return JsonResponse({'error': f'no agreement {id=}'}, status=400, safe=False)

def delete_agreements(request, *args, **kwargs):
    id = request.GET.get('id')
    if Agreement.objects.filter(id=id).exists():
        Agreement.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
