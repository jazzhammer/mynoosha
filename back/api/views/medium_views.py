
from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
import base64
from rest_framework.decorators import api_view

from ..model.medium import Medium, MediumSerializer
from os import path

from ..utils.time_utils import utc_ts

from PIL import Image

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def mediums(request, *args, **kwargs):
    if request.method == 'GET':
        return get_mediums(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_mediums(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_mediums(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_mediums(request, *args, **kwargs):
    search = request.GET.get('search')
    name = request.GET.get('name')
    if name:
        founds = Medium.objects.filter(name=request.GET.get('name'))
    elif search:
        founds = Medium.objects.filter(name__contains=request.GET.get('search'))
    else:
        founds = Medium.objects.all()

    if founds.exists():
        dicts = [model_to_dict(instance) for instance in founds]
        return JsonResponse(dicts, status=200, safe=False)
    else:
        return JsonResponse(
            [],
            status=200,
            safe=False
        )


def post_mediums(request, *args, **kwargs):
    file = request.FILES['image_file']
    name = utc_ts()
    filename = f"mm-{name}.{file.content_type[file.content_type.index('/')+1:]}"
    write_path = path.join(settings.MEDIUMS_FOLDER, filename)
    with open(write_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    im = Image.open(write_path)
    width, height = im.size
    created = Medium.objects.create(filename=filename, width=width, height=height)
    with open(write_path, 'rb') as bfile:
        created_dict = model_to_dict(created)
        created_dict['base64'] = base64.encodebytes(bfile.read()).decode('utf8')

    return JsonResponse(created_dict, status=200, safe=False)

def delete_mediums(request, *args, **kwargs):
    id = request.GET.get('id')
    if Medium.objects.filter(id=id).exists():
        Medium.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
