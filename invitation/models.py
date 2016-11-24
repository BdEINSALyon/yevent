# coding=utf-8
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


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
        if self.type:
            return self.type.default_max_seats
        else:
            return 1

    def __init__(self, *args, **kwargs):
        super(Guest, self).__init__(*args, **kwargs)
        if not self.id:
            self.max_seats = self.type_max_seats()

    max_seats = models.IntegerField()
    last_seen_at = models.DateTimeField(verbose_name='dernière visite', auto_created=True, null=True)

    def available_seats(self):
        order_seats = self.orders.aggregate(count=Coalesce(Sum('seats_count'), 0)).get('count', 0)
        guests_count = self.guests.count()
        return self.max_seats - order_seats - guests_count

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


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
