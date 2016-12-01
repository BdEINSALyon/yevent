from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TicketingConfig(AppConfig):
    name = 'ticketing'
    verbose_name = _('Billets')

