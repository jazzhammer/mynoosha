from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model import WorkInterval
from ..model.invoice import Invoice, InvoiceSerializer
from ..model.invoice_item import InvoiceItem
from ..utils.time_utils import utc_dt


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def invoices(request, *args, **kwargs):
    if request.method == 'GET':
        return get_invoices(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_invoices(request, *args, **kwargs)
    elif request.method == 'PUT':
        return put_invoices(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_invoices(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_invoices(request, *args, **kwargs):
    if request.GET.get('id'):
        try:
            found = Invoice.objects.get(pk=request.GET.get('id'))
        except Exception as dne:
            return JsonResponse({'detail': f'not found for {request.GET.get("id")}'}, status=404, safe=False)
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.GET.get('search'):
        search = request.GET.get('search')
        founds = Invoice.objects.filter(name__contains=search)
        if founds.exists():
            dicts = []
            for instance in founds:
                dict = model_to_dict(instance)
                dict['created'] = str(instance.created)
                dict['issued'] = str(instance.issued)
                dicts.append(dict)
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse(
                {'detail': f'empty result for search={search}'},
                status=404,
                safe=False
            )
    if request.GET.get('client'):
        client = request.GET.get('client')
        founds = Invoice.objects.filter(client__id=client)
        ymdIssueFrom = request.GET.get('ymdIssueFrom')
        if ymdIssueFrom:
            dt_from = utc_dt(iso_format=ymdIssueFrom)
            founds = founds.filter(issued__gte=dt_from)
        ymdIssueThrough = request.GET.get('ymdIssueThrough')
        if ymdIssueThrough:
            dt_through = utc_dt(iso_format=ymdIssueThrough)
            founds = founds.filter(issued__lt=dt_through)
        if founds.exists():
            dicts = []
            for instance in founds:
                dict = model_to_dict(instance)
                dict['created'] = str(instance.created)
                dict['issued'] = str(instance.issued)
                dicts.append(dict)
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse(
                [],
                status=200,
                safe=False
            )
    else:
        founds = Invoice.objects.all()
        dicts = []
        for instance in founds:
            dict = model_to_dict(instance)
            dict['created'] = str(instance.created)
            dict['issued'] = str(instance.issued)
            dicts.append(dict)
        return JsonResponse(
            dicts,
            status=200,
            safe=False)


def post_invoices(request, *args, **kwargs):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        created = serializer.save()
        if request.data.get('issued'):
            created.issued = datetime.fromisoformat(request.data.get("issued"))
        else:
            created.issued = created.created
        created.save()
        dict = model_to_dict(created)
        dict['created'] = str(created.created)
        dict['issued'] = str(created.issued)
        return JsonResponse(dict, status=201, safe=False)
    else:
        return JsonResponse({'error': 'invalid data for Invoice'}, status=400, safe=False)

def put_invoices(request, *args, **kwargs):
    found = Invoice.objects.get(pk=request.data.get('id'))
    dt_issue = datetime.fromisoformat(request.data.get("issued"))
    found.issued = dt_issue
    found.save()
    updated = Invoice.objects.get(pk=request.data.get('id'))
    dict = model_to_dict(updated)
    dict['issued'] = str(updated.issued)
    dict['created'] = str(updated.created)
    return JsonResponse(dict, status=201, safe=False)

def delete_invoices(request, *args, **kwargs):
    id = request.GET.get('id')
    invoice = Invoice.objects.get(pk=id)
    if invoice:
        invoice_items = InvoiceItem.objects.filter(invoice_id=invoice.id)
        for invoice_item in invoice_items:
            work_intervals = WorkInterval.objects.filter(invoice_item_id=invoice_item.id)
            for work_interval in work_intervals:
                work_interval.invoice_item_id = None
                work_interval.save()
            invoice_item.delete()
        invoice.delete()
        return JsonResponse({}, status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
