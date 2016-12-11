import json
import random
import string
from datetime import datetime
from time import time

from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils import timezone
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView

from invitation import email
from invitation import forms
from invitation import models
from invitation import security
from invitation.models import Order


def try_to_reject(guest, request):
    if guest.last_seen_at and (datetime.now() - guest.last_seen_at.replace(tzinfo=None)).seconds < 15:
        # This user is probably logged we render a waiting template
        return SimpleTemplateResponse('invitation/wait.html', {'code': guest.auth_token(), 'next_url': request.path,
                                                               'user_code': guest.code})
    return None


class ShopView(TemplateView):
    template_name = 'invitation/shop.html'
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the URLconf.
    """

    def get(self, request, *args, **params):
        # Load used data
        guest = get_object_or_404(models.Guest, code=params['code'])
        request.session['user_code'] = params['code']
        context = dict()

        # Security code used for the config and ping api
        security_code = security.encrypt({'time': time(), 'user': params['code']})

        # Check and update last seen time
        reject = try_to_reject(guest, request)
        if reject is not None and not settings.DEBUG:
            return reject

        # Update last seen time
        guest.last_seen_at = timezone.now()
        guest.save()

        # Determine reverse to use
        if request.META['HTTP_HOST'] == 'gala.dev.bde-insa-lyon.fr:8000':
            context['shop_url'] = 'https://y.bde-insa-lyon.fr/event/Gala/13095/tickets/widget?' \
                                  'code=GG&default_culture=fr&firstname={first_name}&lastname={last_name}&' \
                                  'email={email}'.format(first_name=guest.first_name, last_name=guest.last_name,
                                                         email=guest.email)
        else:
            context['shop_url'] = 'https://y.bde-insa-lyon.fr/event/Gala/13095/tickets/widget?' \
                                  'from=widget&default_culture=fr&firstname={first_name}&lastname={last_name}&' \
                                  'email={email}'.format(first_name=guest.first_name, last_name=guest.last_name,
                                                         email=guest.email)

        # Add security code to context
        context['code'] = security_code
        context['guest'] = guest

        # Inject limit seats to context
        context['seats_left'] = guest.available_seats()

        return self.render_to_response(context)


class ConfigView(View):
    def get(self, request, *args, **params):
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
            'left_seats': guest.available_seats(),
            'check': settings.SHOP_CHECK_CODE
        }, safe=False)


class PingView(View):
    def get(self, request, *args, **params):
        data = security.decrypt(params['code'])

        # Load Guest from security code
        guest = get_object_or_404(models.Guest, code=data['user'])

        #  Update last seen time
        guest.last_seen_at = timezone.now()
        guest.save()

        return JsonResponse({'success': True, 'code': params['code']}, safe=False)


class CompleteView(View):
    def get(self, request, *args, **params):
        data = security.decrypt(params['code'])

        # Load Guest from security code
        guest = get_object_or_404(models.Guest, code=data['user'])

        success = Order(yurplan_id=request.GET['yurplan_id'], seats_count=int(request.GET['seats_count']),
                        guest=guest).save()

        return JsonResponse({'success': success, 'code': params['code']}, safe=False)


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


class InviteView(FormView):
    template_name = 'invitation/invite.html'
    form_class = forms.GuestForm

    def dispatch(self, request, *args, **kwargs):
        guest = get_object_or_404(models.Guest, code=kwargs['code'])
        request.session['user_code'] = kwargs['code']
        reject = try_to_reject(guest, request)
        if reject is not None:
            return reject
        if guest.invited_by is not None:
            return self.render_to_response({'guest': guest, 'nope': True})
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        sender = models.Guest.objects.get(code=self.request.session['user_code'])

        seats = int(form.cleaned_data['max_seats'])
        if seats > sender.available_seats():
            seats = sender.available_seats()

        guest = models.Guest(
            invited_by=sender,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            max_seats=seats,
            type=models.Type.objects.all().exclude(name='Diplômé').last(),
            code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
        )
        guest.save()
        guest.max_seats = seats
        guest.save()
        email.send_email(guest)

        return self.render_to_response(self.get_context_data(form=forms.GuestForm))

    def get_context_data(self, **kwargs):
        sender = models.Guest.objects.get(code=self.request.session['user_code'])
        kwargs['left_seats'] = sender.available_seats()
        kwargs['guests'] = sender.guests.all()
        kwargs['auth'] = sender.auth_token()
        return super(BaseFormView, self).get_context_data(**kwargs)


class EmailView(View):
    def get(self, request, *args, **kwargs):
        guest = get_object_or_404(models.Guest, code=kwargs['code'])
        template = 'diplome.html'
        if guest.invited_by:
            template = 'invite.html'
        return TemplateResponse(request, 'invitation/email/{}'.format(template),
                                context={'guest': guest, 'host': 'https://gala.dev.bde-insa-lyon.fr'})


class WebhookView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        return HttpResponse('')
