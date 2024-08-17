from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model.project import Project, ProjectSerializer


@api_view(['GET', 'POST', 'DELETE'])
def projects(request, *args, **kwargs):
    if request.method == 'GET':
        return get_projects(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_projects(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_projects(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_projects(request, *args, **kwargs):
    search = request.GET.get('search')
    created_from = request.GET.get('created_from')
    created_through = request.GET.get('created_through')
    client = request.GET.get('client')
    founds = Project.objects.all()
    filtered = False
    if client:
        filtered = True
        founds = founds.filter(agreement__client_id=client)
    if created_from:
        filtered = True
        founds = founds.filter(created__gte=datetime.fromisoformat(created_from))
    if created_through:
        filtered = True
        founds = founds.filter(created__lt=datetime.fromisoformat(created_through))
    if search:
        filtered = True
        founds = founds.filter(name__contains=search)
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

    if filtered:
        # print(founds.query)
        return JsonResponse(
            [model_to_dict(instance) for instance in founds],
            status=200,
            safe=False)
    else:
        return JsonResponse(
            {"detail": "unable to search without filter on name | created | client"},
            status=400,
            safe=False)


def post_projects(request, *args, **kwargs):
    if not Project.objects.filter(name=request.GET.get('name')).exists():
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
        else:
            return JsonResponse({'error': 'invalid data for Project'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'Project already exists'}, status=400, safe=False)

def delete_projects(request, *args, **kwargs):
    id = request.GET.get('id')
    if Project.objects.filter(id=id).exists():
        Project.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
