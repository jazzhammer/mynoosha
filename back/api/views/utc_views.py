from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.utils.time_utils import utc_ts

@api_view(['GET'])
def utc(request, *args, **kwargs):
    iso_format = request.GET.get('iso_format')
    ts = utc_ts(iso_format=iso_format)
    return JsonResponse(ts, status=200, safe=False)