
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model.invoice import Invoice, InvoiceSerializer


@api_view(['GET', 'POST', 'DELETE'])
def invoices(request, *args, **kwargs):
    if request.method == 'GET':
        return get_invoices(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_invoices(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_invoices(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_invoices(request, *args, **kwargs):
    if request.GET.get('search'):
        search = request.GET.get('search')
        founds = Invoice.objects.filter(name__contains=search)
        if founds.exists():
            dicts = [model_to_dict(instance) for instance in founds]
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse(
                {'detail': f'empty result for search={search}'},
                status=404,
                safe=False
            )
    else:
        return JsonResponse(
            [model_to_dict(instance) for instance in Invoice.objects.all().order_by('name')],
            status=200,
            safe=False)


def post_invoices(request, *args, **kwargs):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        created = serializer.save()
        return JsonResponse(model_to_dict(created), status=201, safe=False)
    else:
        return JsonResponse({'error': 'invalid data for Invoice'}, status=400, safe=False)

def delete_invoices(request, *args, **kwargs):
    id = request.GET.get('id')
    if Invoice.objects.filter(id=id).exists():
        Invoice.objects.filter(id=id).delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
