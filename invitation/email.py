import os

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def send_email(guest):
    template = 'diplome.html'
    subject = 'Gala 2017'
    if guest.invited_by:
        template = 'invite.html'
        subject = 'Invitation au Gala 2017'
    html_template = get_template('invitation/email/{}'.format(template))
    text_template = get_template('invitation/email/guest_link.txt')

    d = Context({'guest': guest, 'host': 'https://gala.y.bde-insa-lyon.fr'})

    content = html_template.render(d)
    email = EmailMultiAlternatives(subject, text_template.render(d),
                                   from_email='Gala INSA Lyon <gala.accueil@bde-insa-lyon.fr>', to=[guest.email])
    email.attach_alternative(content, 'text/html')
    email.send()

