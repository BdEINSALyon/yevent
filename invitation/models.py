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
        order_seats = sum(order.tickets.count() for order in self.orders.all())
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


class Type(models.Model):
    class Meta:
        verbose_name = 'type'

    name = models.CharField(max_length=255, verbose_name='nom')
    default_max_seats = models.IntegerField(default=7)

    def __str__(self):
        return self.name
