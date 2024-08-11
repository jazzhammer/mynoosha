from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.utils.time_utils import utc_ts, utc_dt


@api_view(['GET'])
def utc(request, *args, **kwargs):
    iso_format = request.GET.get('iso_format')
    ts = utc_ts(iso_format=iso_format)
    return JsonResponse(ts, status=200, safe=False)

@api_view(['GET'])
def utc_iso(request, *args, **kwargs):
    iso_format = request.GET.get('iso_format')
    dt = utc_dt(iso_format=iso_format)
    result = str(dt)
    result = result.replace('"', '').replace("'", "")
    return JsonResponse(result, status=200, safe=False)