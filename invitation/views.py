from django.views import View
from django.views.generic import TemplateView


class ShopView(TemplateView):
    template_name = 'invitation/shop.html'
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the URLconf.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.META['HTTP_HOST'] == 'gala.dev.bde-insa-lyon.fr:8000':
            context['shop_url'] = 'http://yurplan.bde-insa-lyon.fr:8000/event/Lavage-Ecoflute/12752/tickets/widget?'\
                                  'from=widget&default_culture=fr'
        else:
            context['shop_url'] = 'https://yurplan.bde-insa-lyon.fr/event/Lavage-Ecoflute/12752/tickets/widget?' \
                                  'from=widget&default_culture=fr'
        return self.render_to_response(context)
