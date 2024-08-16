from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..model import WorkType, Invoice, Worker, Agreement
from ..model.worker_rate import WorkerRate, WorkerRateSerializer


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def worker_rates(request, *args, **kwargs):
    if request.method == 'GET':
        return get_worker_rates(request, *args, **kwargs)
    elif request.method == 'POST':
        return post_worker_rates(request, *args, **kwargs)
    elif request.method == 'PUT':
        return put_worker_rates(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return delete_worker_rates(request, *args, **kwargs)
    else:
        return JsonResponse({'data': f"{request.method} unsupported"}, status=400, safe=False)


def get_worker_rates(request, *args, **kwargs):
    id = request.GET.get('id')
    if id:
        try:
            WorkerRate.objects.get(pk=id)
        except Exception:
            return JsonResponse({'detail': f"not found for {id=}"}, status=404, safe=False)

    agreement = request.GET.get('agreement')
    worker = request.GET.get('worker')
    filtered = False
    founds = WorkerRate.objects.all()
    if worker:
        filtered = True
        founds = founds.filter(worker_id=worker)
    if agreement:
        filtered = True
        founds = founds.filter(agreement_id=agreement)
    if filtered:
        if founds.exists():
            return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)
    else:
        return JsonResponse(
            {'detail': 'require search params among: worker | agreement'},
            status=400,
            safe=False
        )


def post_worker_rates(request, *args, **kwargs):
    worker = request.data.get('worker')
    agreement = request.data.get('agreement')
    amount_rate = request.data.get('amount_rate')
    if worker and agreement:
        worker_rate = WorkerRate.objects.create(
            worker=Worker.objects.get(pk=worker),
            agreement=Agreement.objects.get(pk=agreement),
            amount_rate=int(amount_rate)
        )
        return JsonResponse(model_to_dict(worker_rate), status=201, safe=False)
    else:
        return JsonResponse(None, safe=False, status=400)


def put_worker_rates(request, *args, **kwargs):
    found = WorkerRate.objects.get(pk=request.data.get('id'))
    worker = request.data.get('worker')
    agreement = request.data.get('agreement')
    amount_rate = request.data.get('amount_rate')

    if amount_rate:
        found.amount_rate = amount_rate
    if agreement:
        found.agreement = Agreement.objects.get(pk=agreement)
    if worker:
        found.worker = Worker.objects.get(pk=int(worker))
    found.save()
    updated = WorkerRate.objects.get(pk=request.data.get('id'))
    return JsonResponse(model_to_dict(updated), status=200, safe=False)


def delete_worker_rates(request, *args, **kwargs):
    id = request.GET.get('id')
    try:
        worker_rate = WorkerRate.objects.get(pk=id)
        worker_rate.delete()
    except:
        return JsonResponse({'error': f'not found to delete: {id=}'}, status=404, safe=False)
    else:
        return JsonResponse(model_to_dict(worker_rate), status=200, safe=False)
