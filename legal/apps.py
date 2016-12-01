from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LegalConfig(AppConfig):
    name = 'legal'
    verbose_name = _('Légal')

