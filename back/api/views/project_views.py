from datetime import datetime

from django.db.models import QuerySet, Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view

from ..model import Client, Agreement
from ..model.project import Project, ProjectSerializer


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def projects(request, *args, **kwargs):
    if request.method == 'GET':
        return get_projects(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_projects(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_projects(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)

def put_projects(request: HttpRequest):
    started = request.POST.get('started')
    finished = request.POST.get('finished')

    client = request.POST.get('client')
    agreement = request.POST.get('agreement')

    name = request.POST.get('name')
    description = request.POST.get('description')

    id = request.POST.get('id')
    errors = []
    if id:
        found = Project.objects.get(pk=id)
        if started:
            found.started = datetime.fromisoformat(started)
        if finished:
            found.started = datetime.fromisoformat(finished)
        if name:
            found.name = name
        if description:
            found.description = name
        if client:
            try:
                found.client = Client.objects.get(pk=client)
            except:
                errors.append(f'failed to update Project.Client for {client=}')
        if agreement:
            try:
                found.agreement = Agreement.objects.get(pk=agreement)
            except:
                errors.append(f'failed to update Project.Agreement for {agreement=}')
        if len(errors) > 0:
            return JsonResponse({"details": errors}, status=400, safe=False)
        else:
            found.save()
            return JsonResponse(model_to_dict(found), status=200, safe=False)
    else:
        return JsonResponse({"detail": f"unable to update project for {id=}"}, status=400, safe=False)

def get_projects(request: HttpRequest, *args, **kwargs):
    search = request.GET.get('search')
    created_from = request.GET.get('created_from')
    created_through = request.GET.get('created_through')
    client = request.GET.get('client')
    client_name = request.GET.get('client_name')
    founds = Project.objects.all()
    pre_start = request.GET.get('pre_start')
    post_start = request.GET.get('post_start')
    pre_finish = request.GET.get('pre_finish')
    post_finish = request.GET.get('post_finish')
    filtered = False
    if pre_finish:
        filtered = True
        founds = founds.filter(finished__gte=datetime.fromisoformat(pre_finish))
    if post_finish:
        filtered = True
        founds = founds.filter(finished__lt=datetime.fromisoformat(post_finish))
    if pre_start:
        filtered = True
        founds = founds.filter(started__gte=datetime.fromisoformat(pre_start))
    if post_start:
        filtered = True
        founds = founds.filter(started__lt=datetime.fromisoformat(post_start))
    if client:
        filtered = True
        founds = founds.filter(Q(agreement__client_id=client) | Q(client_id=client))
    if client_name:
        filtered = True
        founds = founds.filter(client__name__contains=client_name)
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
                dict['created'] = instance.created
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
        dicts = []
        for instance in founds:
            dict = model_to_dict(instance)
            dict['created'] = instance.created
            dicts.append(dict)

        return JsonResponse(
            dicts,
            status=200,
            safe=False)
    else:
        return JsonResponse(
            {"detail": "unable to search without filter on name | created | client"},
            status=400,
            safe=False)


def post_projects(request, *args, **kwargs):
    name = request.data.get('name')
    description = request.data.get('description')
    client = request.data.get('client')
    agreement = request.data.get('agreement')
    # check dupes for client and name
    if name and description and client:
        already: QuerySet = Project.objects.filter(name=name, client_id=client)
        if already.exists() and already.count() > 0:
            return JsonResponse({'error': f'Project "{name}" already exists for client {client}'}, status=400, safe=False)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created = serializer.save()
            return JsonResponse(model_to_dict(created), status=201, safe=False)
        else:
            return JsonResponse({'error': 'invalid data for Project'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'Project requires name, description and client'}, status=400, safe=False)

def delete_projects(request, *args, **kwargs):
    id = request.GET.get('id')
    if Project.objects.filter(id=id).exists():
        Project.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
