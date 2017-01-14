from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic.edit import ModelFormMixin

from invitation.models import Guest
from waitlist.forms import WaitingTicketForm
from waitlist.models import WaitingTicket


def max_for(guest):
    return guest.available_seats() - WaitingTicket.objects.filter(owner=guest, used=False).aggregate(Sum('amount'))['amount__sum']


class ListWaitRegistrations(ListView):
    model = WaitingTicket
    template_name = 'waitlist/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=Guest.objects.get(code=self.request.session['user_code']))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        guest = Guest.objects.get(code=self.request.session['user_code'])
        data.update({
            'left_seats': max_for(guest),
            'form': WaitingTicketForm()
        })
        return data


class CreateWaitRegistration(CreateView):
    model = WaitingTicket
    form_class = WaitingTicketForm
    template_name = 'waitlist/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        guest = Guest.objects.get(code=self.request.session['user_code'])
        data.update({
            'left_seats': max_for(guest),
            'form': WaitingTicketForm()
        })
        return data

    def form_valid(self, form):
        ticket = form.instance
        ticket.owner = Guest.objects.get(code=self.request.session['user_code'])
        if ticket.amount > max_for(ticket.owner):
            ticket.amount = max_for(ticket.owner)
        ticket.save()
        return HttpResponseRedirect(reverse_lazy('waitlist'))


class DeleteWaitRegistration(DeleteView):
    model = WaitingTicket
    success_url = reverse_lazy('waitlist')
    template_name = 'waitlist/delete.html'
