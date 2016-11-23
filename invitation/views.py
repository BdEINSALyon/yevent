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
        return self.render_to_response(context)