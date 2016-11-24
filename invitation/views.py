from time import time

from django.shortcuts import get_object_or_404
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
        guest = get_object_or_404(models.Guest, code=params['code'])
        context = dict()
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
        context['code'] = security.encrypt({'time': time(), 'user': params['code']})
        return self.render_to_response(context)


