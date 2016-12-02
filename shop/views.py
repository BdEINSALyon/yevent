import itertools

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from invitation import session
from invitation.session import get_guest
from questions.models import Answer
from shop.models import Order
from ticketing.models import Price, Ticket, OptionSelection


def _has_waiting_order_not_in(request, status=''):
    guest = get_guest(request)
    return guest.orders.filter(~Q(status='PAID')).count() >= 1 and not guest.orders.filter(~Q(status='PAID')).last().status == status


def _redirect_to_not_in(request, status=''):
    guest = get_guest(request)
    return redirect('shop.{}'.format(guest.orders.filter(~Q(status=['PAID', status])).first().status.lower()))


class CartView(TemplateView):
    status = 'NONE'

    def dispatch(self, request, *args, **kwargs):
        if _has_waiting_order_not_in(request, self.status):
            return _redirect_to_not_in(request, self.status)
        if self.order(request) is None and self.status != 'ONGOING':
            return redirect('shop.ongoing')
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def guest(request):
        return get_guest(request)

    def order(self, request):
        return CartView.guest(request).orders.filter(status=self.status).last()


class CartSelectionView(CartView):
    status = 'ONGOING'
    template_name = 'shop/products_select.html'

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        guest = get_guest(request)
        if _has_waiting_order_not_in(request, 'ONGOING'):
            return _redirect_to_not_in(request, 'ONGOING')

        order = Order(guest=guest, status='ONGOING')
        order.save()
        for price in Price.objects.all():
            for _ in itertools.repeat(None, int('0'+request.POST['seats_{}'.format(price.id)])):
                if Ticket.objects.filter(price=price).count() >= price.limit:
                    messages.error(request, _("Un produit demandé n'est plus disponible, veuillez repasser la commande."))
                    for ticket in order.tickets:
                        ticket.delete()
                    order.delete()
                    return redirect('shop.ongoing')
                else:
                    ticket = Ticket(order=order, price=price)
                    ticket.save()
                    order.tickets.add(ticket)
        order.status = 'QUESTIONS'
        order.save()

        return redirect('shop.questions')

    def get(self, request, *args, **kwargs):
        get_guest(request)
        if _has_waiting_order_not_in(request, 'ONGOING'):
            return _redirect_to_not_in(request, 'ONGOING')
        context = {
            'prices': Price.objects.all,
            'allowed_amounts': range(0, 8),
            'state': 'ONGOING'
        }
        return self.render_to_response(context)


class CartQuestionView(CartView):
    template_name = 'shop/questions.html'
    status = 'QUESTIONS'

    # noinspection PyMethodMayBeStatic
    def post(self, request):

        order = self.order(request)

        error = False

        for ticket in order.tickets.all():
            post_key = 'ticket_{}_'.format(ticket.id)
            ticket.first_name = request.POST['{}first_name'.format(post_key)]
            ticket.last_name = request.POST['{}last_name'.format(post_key)]

            if ticket.first_name == '' or ticket.last_name == '':
                error = True

            for question in ticket.price.required_questions.all():
                q_post_key = '{}answer_for_{}'.format(post_key, question.id)
                answer = Answer(question=question, data=request.POST.get(q_post_key, ''))
                answer.save()
                ticket.answers.add(answer)

            for option in ticket.price.allowed_options.all():
                desired = int(request.POST.get('{}option_{}'.format(post_key, option.id), '0'))
                selection = OptionSelection.objects.get_or_create(ticket=ticket, option=option)
                selection[0].seats = desired
                selection[0].save()

            ticket.save()

        if not error:
            order.status = 'PAYMENT'
            order.save()

        return redirect('shop.questions')

    def get(self, request, *args, **kwargs):
        guest = get_guest(request)
        order = guest.orders.filter(status='QUESTIONS').last()
        context = {
            'order': order,
            'state': 'QUESTIONS'
        }
        return self.render_to_response(context)
