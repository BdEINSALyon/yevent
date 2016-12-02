from time import time

from invitation import security
from invitation.models import Guest


def set_guest(request, guest):
    request.session['guest'] = security.encrypt({'id': guest.id, 'time': time()})


def get_guest(request):
    ticket = security.decrypt(request.session['guest'])
    # noinspection PyBroadException
    try:
        if time() - ticket['time'] < 3600:

            # Session ticket is valid 1 hour
            guest = Guest.objects.get(id=ticket['id'])
            set_guest(request, guest)
            return guest
        else:
            return None
    except:
        return None
