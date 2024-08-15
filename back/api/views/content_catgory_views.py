from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime

from ..model import Agreement
from ..model.content_category import ContentCategory, ContentCategorySerializer

from django.utils import timezone
import pytz

from ..utils.time_utils import utc_dt

timezone.activate(pytz.timezone('UTC'))

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def content_categorys(request, *args, **kwargs):
    if request.method == 'GET':
        return get_content_categorys(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_content_categorys(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_content_categorys(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_content_categorys(request, *args, **kwargs):
    search = request.GET.get('search')
    name = request.GET.get('name')
    founds = ContentCategory.objects.all()
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
    if filtered and founds.exists():
        return JsonResponse([model_to_dict(instance) for instance in founds], safe=False, status=200)
    else:
        return JsonResponse(
            [],
            status=200,
            safe=False
        )


def post_content_categorys(request, *args, **kwargs):
    search = request.data.get("search")
    name = request.data.get("name")
    already = ContentCategory.objects.all()
    filtered = False
    if search:
        filtered = True
        already = already.filter(name__contains=search)
    if name:
        filtered = True
        already = already.filter(name=name)
    if filtered:
        if already.exists():
            return JsonResponse({'error': 'ContentCategory already exists'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'require last_name | first_name | ymd_birth to rule out duplicates'}, status=400, safe=False)

    created = ContentCategory.objects.create(
        name=name,
    )
    return JsonResponse(model_to_dict(created), status=201, safe=False)

def delete_content_categorys(request, *args, **kwargs):
    id = request.GET.get('id')
    content_category = ContentCategory.objects.get(pk=id)
    deleted = 0
    if content_category:
        agreements = Agreement.objects.filter(content_category_id=id)
        for agreement in agreements:
            agreement.delete()
            deleted += 1
        content_category.delete()
    return JsonResponse({'detail': f'{deleted}'}, status=200, safe=False)
