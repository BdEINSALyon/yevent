from django import forms
from django.forms import ModelForm

from waitlist.models import WaitingTicket


class WaitingTicketForm(ModelForm):
    class Meta:
        model = WaitingTicket
        fields = ['waiting_list', 'amount', 'phone']
