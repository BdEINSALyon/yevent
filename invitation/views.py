from datetime import datetime
from time import time

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import SimpleTemplateResponse
from django.utils.timezone import utc
from django.views import View
from django.views.generic import TemplateView

from invitation import models
from invitation import security


class ShopView(TemplateView):
    template_name = 'invitation/shop.html'
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the URLconf.
    """
    def get(self, request, *args, **params):
        # Load used data
        guest = get_object_or_404(models.Guest, code=params['code'])
        context = dict()

        # Security code used for the config and ping api
        security_code = security.encrypt({'time': time(), 'user': params['code']})

        # Check and update last seen time
        if guest.last_seen_at and (datetime.now() - guest.last_seen_at.replace(tzinfo=None)).seconds < 15:
            # This user is probably logged we render a waiting template
            return SimpleTemplateResponse('invitation/wait.html', {'code': security_code})

        # Update last seen time
        guest.last_seen_at = datetime.utcnow()
        guest.save()

        # Determine reverse to use
        if request.META['HTTP_HOST'] == 'gala.dev.bde-insa-lyon.fr:8000':
            context['shop_url'] = 'http://yurplan.bde-insa-lyon.fr:8000/event/Lavage-Ecoflute/12752/tickets/widget?'\
                                  'from=widget&default_culture=fr&firstname={first_name}&lastname={last_name}&' \
                                  'email={email}'.format(first_name=guest.first_name, last_name=guest.last_name,
                                                         email=guest.email)
        else:
            context['shop_url'] = 'https://yurplan.bde-insa-lyon.fr/event/Lavage-Ecoflute/12752/tickets/widget?' \
                                  'from=widget&default_culture=fr&firstname={first_name}&lastname={last_name}&' \
                                  'email={email}'.format(first_name=guest.first_name, last_name=guest.last_name,
                                                         email=guest.email)

        # Add security code to context
        context['code'] = security_code

        return self.render_to_response(context)


class ConfigView(View):
    def get(self,request, *args, **params):
        data = security.decrypt(params['code'])
        guest = get_object_or_404(models.Guest, code=data['user'])
        return JsonResponse({
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'invited_by': guest.invited_by and {
                'first_name': guest.invited_by.first_name,
                'last_name': guest.invited_by.last_name
            } or None,
            'max_seats': guest.max_seats,
            'left_seats': guest.available_seats()
        }, safe=False)


class PingView(View):
    def get(self,request, *args, **params):
        data = security.decrypt(params['code'])

        # Load Guest from security code
        guest = get_object_or_404(models.Guest, code=data['user'])

        #  Update last seen time
        guest.last_seen_at = datetime.utcnow()
        guest.save()

        return JsonResponse({'success': True, 'code': params['code']}, safe=False)


class AvailableView(View):
    def get(self, request, *arg, **params):
        data = security.decrypt(params['code'])

        # Load Guest from security code
        guest = get_object_or_404(models.Guest, code=data['user'])

        return JsonResponse({
            'success': (not guest.last_seen_at) or
                       (datetime.now() - guest.last_seen_at.replace(tzinfo=None)).seconds >= 15,
            'code': params['code']
        }, safe=False)