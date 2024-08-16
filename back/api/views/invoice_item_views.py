from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model import WorkType, Invoice, WorkInterval
from ..model.invoice_item import InvoiceItem, InvoiceItemSerializer
from ..model.work_interval import WorkIntervalSerializer, work_interval_hhmm


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def invoice_items(request, *args, **kwargs):
    if request.method == 'GET':
        return get_invoice_items(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_invoice_items(request, *args, **kwargs)
    elif request.method == 'PUT':
        return put_invoice_items(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_invoice_items(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_invoice_items(request, *args, **kwargs):
    id = request.GET.get('id')
    if id:
        try:
            InvoiceItem.objects.get(pk=id)
        except Exception:
            return JsonResponse({'detail': f"not found for {id=}"}, status=404, safe=False)

    search = request.GET.get('search')
    detail = request.GET.get('detail')
    invoice = request.GET.get('invoice')
    work_type = request.GET.get('work_type')
    filtered = False
    founds = InvoiceItem.objects.all()
    if search or detail:
        filtered = True
        if search:
            founds = founds.filter(detail__contains=search)
        else:
            founds = founds.filter(detail__contains=detail)
    if invoice:
        filtered = True
        founds = founds.filter(invoice_id=invoice)
    if work_type:
        filtered = True
        founds = founds.filter(work_type_id=work_type)
    if filtered:
        if founds.exists():
            dicts = []
            for instance in founds:
                adict = model_to_dict(instance)
                work_intervals = WorkInterval.objects.filter(invoice_item_id=instance.id)
                if (work_intervals.exists()):
                    work_interval = work_intervals.first()
                    work_interval_dict = model_to_dict(work_interval)
                    adict['work_interval'] = work_interval_dict
                    adict['work_interval']['hhmm'] = work_interval_hhmm(work_interval_dict.get('start_utcms'), work_interval_dict.get('stop_utcms'))
                dicts.append(adict)
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)
    else:
        return JsonResponse(
            {'detail': 'require search params among: invoice | work_type | detail'},
            status=400,
            safe=False
        )

'''
connecting invoices and invoicables type = workinterval / time / milestones
amounts are calculated differently for each
'''
def post_invoice_items(request, *args, **kwargs):
    invoice = request.data.get('invoice')
    work_interval = request.data.get('work_interval')
    work_type = request.data.get('work_type')

    if invoice and work_interval and work_type:

        invoice_item = InvoiceItem.objects.create(
            invoice=Invoice.objects.get(pk=invoice),
            work_type=WorkType.objects.get(pk=work_type)
        )
        created_invoice_item = model_to_dict(invoice_item)
        # update the work_interval for invoice_item
        work_interval = WorkInterval.objects.get(pk=work_interval)
        work_interval.invoice_item = invoice_item
        work_interval.save()
        # calculate the amount
        # agreement connects client + worker
        # work_intervals are performed by a worker for a client
        return JsonResponse(created_invoice_item, status=201, safe=False)
    else:
        return JsonResponse(None, safe=False, status=400)


def put_invoice_items(request, *args, **kwargs):
    found = InvoiceItem.objects.get(pk=request.data.get('id'))
    amount_total = request.data.get('amount_total')
    detail = request.data.get('detail')
    work_type = request.data.get('work_type')

    if amount_total:
        found.amount_total = amount_total
    if detail:
        found.detail = detail
    if work_type:
        work_type = WorkType.objects.get(pk=int(work_type))
        found.work_type = work_type
    found.save()
    updated = InvoiceItem.objects.get(pk=request.data.get('id'))
    dict = model_to_dict(updated)
    return JsonResponse(dict, status=200, safe=False)


def delete_invoice_items(request, *args, **kwargs):
    id = request.GET.get('id')
    invoice_item = InvoiceItem.objects.get(pk=id)
    if invoice_item:
        # remove references by workintervals
        work_intervals = WorkInterval.objects.filter(invoice_item_id=id)
        deleted_work_intervals = 0
        for work_interval in work_intervals:
            work_interval.invoice_item = None
            work_interval.save()
            deleted_work_intervals += 1
        invoice_item.delete()
        return JsonResponse(model_to_dict(invoice_item), status=200, safe=False)
    else:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
    # if InvoiceItem.objects.filter(id=id).exists():
    #     InvoiceItem.objects.filter(id=id).delete()
    #     return JsonResponse({}, status=200, safe=False)
    # else:
    #     return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
