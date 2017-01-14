from django import forms
from django.forms import ModelForm, ModelChoiceField

from waitlist.models import WaitingTicket, WaitingList


class WaitingTicketForm(ModelForm):
    waiting_list = ModelChoiceField(queryset=WaitingList.objects.filter(enabled=True), empty_label=None)

    class Meta:
        model = WaitingTicket
        fields = ['waiting_list', 'amount', 'phone']
