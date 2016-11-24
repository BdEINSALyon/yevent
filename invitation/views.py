from time import time

from django.views import View
from django.views.generic import TemplateView

from invitation import security


class ShopView(TemplateView):
    template_name = 'invitation/shop.html'
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the URLconf.
    """
    def get(self, request, *args, **params):
        context = dict()
        if request.META['HTTP_HOST'] == 'gala.dev.bde-insa-lyon.fr:8000':
            context['shop_url'] = 'http://yurplan.bde-insa-lyon.fr:8000/event/Lavage-Ecoflute/12752/tickets/widget?'\
                                  'from=widget&default_culture=fr'
        else:
            context['shop_url'] = 'https://yurplan.bde-insa-lyon.fr/event/Lavage-Ecoflute/12752/tickets/widget?' \
                                  'from=widget&default_culture=fr'
        context['code'] = security.encrypt({'time': time(), 'user': params['code']})
        return self.render_to_response(context)
