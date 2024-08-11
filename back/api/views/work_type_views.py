
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model.work_type import WorkType, WorkTypeSerializer


@api_view(['GET', 'POST', 'DELETE'])
def work_types(request, *args, **kwargs):
    if request.method == 'GET':
        return get_work_types(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_work_types(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_work_types(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_work_types(request, *args, **kwargs):
    search = request.GET.get('search')
    name = request.GET.get('name')
    if name:
        founds = WorkType.objects.filter(name=request.GET.get('name'))
    elif search:
        founds = WorkType.objects.filter(name__contains=request.GET.get('search'))
    else:
        founds = WorkType.objects.all()

    if founds.exists():
        dicts = [model_to_dict(instance) for instance in founds]
        return JsonResponse(dicts, status=200, safe=False)
    else:
        return JsonResponse(
            [],
            status=200,
            safe=False
        )

def post_work_types(request, *args, **kwargs):
    name = request.data['name']
    model_found = WorkType.objects.filter(name=name).first()
    if not model_found:
        serializer = WorkTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
        else:
            return JsonResponse({'error': 'invalid data for WorkType'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'WorkType already exists'}, status=400, safe=False)

def delete_work_types(request, *args, **kwargs):
    id = request.GET.get('id')
    if WorkType.objects.filter(id=id).exists():
        WorkType.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
