from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InvitationConfig(AppConfig):
    name = 'invitation'
    verbose_name = _('Invitations')

