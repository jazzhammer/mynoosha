from datetime import datetime

from django.db.models import QuerySet, Q
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
    id = request.GET.get('id')
    if id:
        try:
            found = Agreement.objects.get(pk=id)
            return JsonResponse(model_to_dict(found), status=200, safe=False)
        except:
            return JsonResponse({"detail": f"none found for {id=}"}, status=404, safe=False)

    client = request.GET.get('client')
    name = request.GET.get('name')
    search = request.GET.get('search')
    type = request.GET.get('type')
    created_from = request.GET.get("created_from")
    created_through = request.GET.get("created_through")

    founds = Agreement.objects.all()
    filtered = False
    if search:
        filtered = True
        if search.isnumeric():
            founds = founds.filter(Q(name__contains=search) | Q(id=int(search)))
        else:
            founds = founds.filter(name__contains=search)
    if name:
        filtered = True
        founds = founds.filter(name=name)
    if client:
        filtered = True
        founds = founds.filter(client_id=client)
    if type:
        filtered = True
        founds = founds.filter(type=type)
    if created_from:
        filtered = True
        founds = founds.filter(created__gte=datetime.fromisoformat(created_from))
    if created_through:
        filtered = True
        founds = founds.filter(created__lte=datetime.fromisoformat(created_through))

    if filtered:
        if founds.exists():
            dicts = []
            for instance in founds:
                instance_dict = model_to_dict(instance)
                instance_dict['created'] = instance.created
                dicts.append(instance_dict)
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)
    else:
        return JsonResponse(
            {'detail': f'empty result for search parameters {client=}, {type=}, {name=}'},
            status=200,
            safe=False
        )

def post_agreements(request, *args, **kwargs):
    name: str = request.GET.get('name')
    if name:
        name = name.strip()
        if len(name) > 0:
            if not Agreement.objects.filter(name=name).exists():
                serializer = AgreementSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    created = serializer.save()
                    return JsonResponse(model_to_dict(created), status=201, safe=False)
                else:
                    return JsonResponse({'error': 'invalid data for Agreement'}, status=400, safe=False)
            else:
                return JsonResponse({'error': 'Agreement already exists'}, status=400, safe=False)
        else:
            return JsonResponse({'error': 'require non-blank name for agreement'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'require name for agreement'}, status=400, safe=False)


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
        type = request.data.get('type')
        if name:
            agreement.name = name
        if client:
            agreement.client = Client.objects.get(pk=client)
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

@api_view(['GET'])
def agreements_count(request, *args, **kwargs):
    client = request.GET.get("client")
    founds: QuerySet = Agreement.objects.all()
    filtered = False
    if client:
        filtered = True
        founds = founds.filter(client_id=client)

    if filtered:
        return JsonResponse(founds.count(), status=200, safe=False)
    else:
        return JsonResponse({"details": "require filter by client for count"}, status=400, safe=False)

