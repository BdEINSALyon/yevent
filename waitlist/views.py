from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from invitation.models import Guest
from waitlist.models import WaitingTicket


class ListWaitRegistrations(ListView):
    model = WaitingTicket
    template_name = 'waitlist/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=Guest.objects.get(code=self.request.session['user_code']))


class CreateWaitRegistration(CreateView):
    model = WaitingTicket


class DeleteWaitRegistration(DeleteView):
    model = WaitingTicket
