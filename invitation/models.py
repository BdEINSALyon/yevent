# coding=utf-8
import string
from random import random
from time import time

from django.core import urlresolvers
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

from invitation import security


class Guest(models.Model):
    class Meta:
        verbose_name = 'invité'

    first_name = models.CharField(max_length=255, verbose_name='prénom')
    last_name = models.CharField(max_length=255, verbose_name='nom')
    code = models.CharField(max_length=255, verbose_name='code', default='', unique=True)
    email = models.EmailField(blank=True)
    invited_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='invité par',
        related_name='guests'
    )
    type = models.ForeignKey(
        'Type',
        null=False,
        blank=False,
        verbose_name='type'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def type_max_seats(self):
        try:
            if self.type:
                return self.type.default_max_seats
            else:
                return 1
        except:
            return 1

    def __init__(self, *args, **kwargs):
        super(Guest, self).__init__(*args, **kwargs)
        if not self.id:
            self.max_seats = self.type_max_seats()

    max_seats = models.IntegerField()
    last_seen_at = models.DateTimeField(verbose_name='dernière visite', auto_created=True, blank=True, null=True)

    def available_seats(self):
        order_seats = self.orders.aggregate(count=Coalesce(Sum('seats_count'), 0)).get('count', 0)
        guests_count = self.guests.aggregate(count=Coalesce(Sum('max_seats'), 0)).get('count', 0)
        return self.max_seats - order_seats - guests_count

    def auth_token(self):
        return security.encrypt({'time': time(), 'user': self.code})

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def generate_code(self):
        if self.code == '' or self.code is None:
            while True:
                code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
                if Guest.objects.filter(code=code).count() < 1:
                    break

    def send_email(self):
        msg = EmailMultiAlternatives(
            subject="Gala INSA Lyon 2017",
            body="Accedez à la boutique : {}".format(urlresolvers.reverse('shop', {'code': self.code})),
            from_email="Example <admin@example.com>",
            to=["New User <user1@example.com>", "account.manager@example.com"],
            reply_to=["Helpdesk <support@example.com>"])

        # Include an inline image in the html:
        logo_cid = attach_inline_image_file(msg, "/path/to/logo.jpg")
        html = """<img alt="Logo" src="cid:{logo_cid}">
                  <p>Please <a href="http://example.com/activate">activate</a>
                  your account</p>""".format(logo_cid=logo_cid)
        msg.attach_alternative(html, "text/html")

        # Optional Anymail extensions:
        msg.metadata = {"user_id": "8675309", "experiment_variation": 1}
        msg.tags = ["activation", "onboarding"]
        msg.track_clicks = True

        # Send it:
        msg.send()


class Type(models.Model):
    class Meta:
        verbose_name = 'type'

    name = models.CharField(max_length=255, verbose_name='nom')
    default_max_seats = models.IntegerField(default=7)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'commande'

    yurplan_id = models.CharField(max_length=100, verbose_name='ID Yurplan')
    seats_count = models.IntegerField(verbose_name='nombre de places')
    guest = models.ForeignKey(
        'Guest',
        null=False,
        blank=False,
        related_name='orders'
    )
