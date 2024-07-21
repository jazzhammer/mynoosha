import json

from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def clients(request):
    if request.method == 'GET':
        return JsonResponse(json.dumps({'data': 'ok'}), status=200, safe=False)
    else:
        return JsonResponse(json.dumps({'data': 'POST unsupported'}), status=200, safe=False)