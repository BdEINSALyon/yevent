from django.http import JsonResponse
from django.utils import timezone

from invitation import models


def ping(request, *args, **params):
    guest = models.Guest.objects.get(code=request.session['user_code'])

    #  Update last seen time
    guest.last_seen_at = timezone.now()
    guest.save()

    return JsonResponse({'success': True}, safe=False)


def halt(request):
    guest = models.Guest.objects.get(code=request.session['user_code'])

    #  Update last seen time
    guest.last_seen_at = None
    guest.save()

    return JsonResponse({'success': True}, safe=False)
