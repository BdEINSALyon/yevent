from django.http import JsonResponse
from django.utils import timezone

from ticketing import models


def prices(request, *args, **params):
    all_prices = models.Price.objects.all()
    data = {}
    for price in all_prices:
        data[price.id] = price.to_object()
    return JsonResponse(data, safe=False)
