# coding=utf-8
import random
import string
from datetime import timedelta, datetime
from threading import Thread
from time import time

from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce

from invitation import security
from invitation import yurplan


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
    email_received = models.BooleanField(default=False, verbose_name='email envoyé')

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

    max_seats = models.IntegerField(verbose_name='places')
    last_seen_at = models.DateTimeField(verbose_name='dernière visite', auto_created=True, blank=True, null=True)

    def available_seats(self):
        order_seats = self.orders.filter(Q(status=0, created_at__gte=(datetime.now() - timedelta(minutes=4))) | Q(status=1)).aggregate(count=Coalesce(Sum('seats_count'), 0)).get('count', 0)
        guests_count = self.guests.aggregate(count=Coalesce(Sum('max_seats'), 0)).get('count', 0)
        return self.max_seats - order_seats - guests_count

    available_seats.verbose_name = 'places restantes'

    def auth_token(self):
        return security.encrypt({'time': time(), 'user': self.code})

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def generate_code(self):
        if self.code == '' or self.code is None:
            while True:
                self.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
                if Guest.objects.filter(code=self.code).count() < 1:
                    break


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
    status = models.IntegerField(verbose_name='statut de la commande', choices=((0, 'En cours'), (1, 'payée'), (2, 'annulée'), (3, 'annulée (délais)')))
    created_at = models.DateTimeField(auto_now_add=True)
    guest = models.ForeignKey(
        'Guest',
        null=False,
        blank=False,
        related_name='orders'
    )

    def load_from_api(self):
        RefreshOrderThread(self).start()

    def __str__(self):
        return "{} ({})".format(self.yurplan_id, self.guest)


class RefreshOrderThread(Thread):

    def __init__(self, order):
        super().__init__()
        self.order = order

    def run(self):
        import time
        while self.order.status == 0:
            yurplan_order = yurplan.ApiClient().get_order(self.order.yurplan_id)
            self.order.status = yurplan_order['status']
            self.order.save()
            time.sleep(5)
