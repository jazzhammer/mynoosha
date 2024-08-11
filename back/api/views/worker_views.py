from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime

from ..model.worker import Worker, WorkerSerializer

from django.utils import timezone
import pytz

from ..utils.time_utils import utc_dt

timezone.activate(pytz.timezone('UTC'))

@api_view(['GET', 'POST', 'DELETE'])
def workers(request, *args, **kwargs):
    if request.method == 'GET':
        return get_workers(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_workers(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_workers(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_workers(request, *args, **kwargs):
    search = request.GET.get('search')
    name = request.GET.get('name')
    last_name = request.GET.get('last_name')
    first_name = request.GET.get('first_name')
    ymd_birth = request.GET.get('ymd_birth')
    founds = Worker.objects.all()
    filterd = False
    if search or name:
        filtered = True
        if search:
            founds = founds.filter(
                Q(last_name__contains=search) | Q(first_name__contains=search)
            )
        elif name:
            founds = founds.filter(
                Q(last_name=name) | Q(first_name=name)
            )
        if ymd_birth:
            utc_birth = utc_dt(ymd_birth)
            founds = founds.filter(ymd_birth=utc_birth)
        if founds.exists():
            dicts = []
            for instance in founds:
                dict = model_to_dict(instance)
                dict['created'] = str(instance.created)
                dicts.append(dict)
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse(
                [],
                status=200,
                safe=False
            )
    elif last_name or first_name:
        filtered = True
        if last_name:
            founds = founds.filter(last_name=last_name)
        if first_name:
            founds = founds.filter(first_name=first_name)
    if filtered and founds.exists():
        return JsonResponse([model_to_dict(instance) for instance in founds], safe=False, status=200)
    else:
        return JsonResponse(
            [],
            status=200,
            safe=False
        )


def post_workers(request, *args, **kwargs):
    search = request.data.get("search")
    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')
    ymd_birth = request.data.get('ymd_birth')
    already = Worker.objects.all()
    filtered = False
    if ymd_birth:
        dt_birth = datetime.fromisoformat(ymd_birth)
        already = already.filter(ymd_birth=dt_birth)
        filtered = True
    if last_name:
        already = already.filter(last_name=last_name)
        filtered = True
    if first_name:
        already = already.filter(first_name=first_name)
        filtered = True
    if search:
        already = already.filter(Q(first_name__contains=search) | Q(last_name__contains=search))
        filtered = True
    if filtered:
        if already.exists():
            return JsonResponse({'error': 'Worker already exists'}, status=400, safe=False)
        else:
            pass
    else:
        return JsonResponse({'error': 'require last_name | first_name | ymd_birth to rule out duplicates'}, status=400, safe=False)

    can_create = last_name and first_name and ymd_birth
    if can_create:
        created = Worker.objects.create(
            last_name=last_name,
            first_name=first_name,
            ymd_birth=datetime.fromisoformat(ymd_birth)
        )
        return JsonResponse(model_to_dict(created), status=201, safe=False)
    else:
        return JsonResponse({'error': 'Worker requires last_name, first_name, ymd_birth'}, status=400, safe=False)

def delete_workers(request, *args, **kwargs):
    id = request.GET.get('id')
    if Worker.objects.filter(id=id).exists():
        Worker.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
