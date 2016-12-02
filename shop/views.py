from django.views.generic import TemplateView

from invitation import session
from invitation.session import get_guest
from ticketing.models import Price


class CartSelectionView(TemplateView):
    template_name = 'shop/products_select.html'

    def get(self, request, *args, **kwargs):
        get_guest(request)
        context = {
            'prices': Price.objects.all,
            'allowed_amounts': range(0, 8),
            'state': 'ONGOING'
        }
        return self.render_to_response(context)
