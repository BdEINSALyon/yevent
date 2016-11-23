# coding=utf-8
from django.db import models


class Guest(models.Model):
    class Meta:
        verbose_name = 'invité'

    name = models.CharField(max_length=255, verbose_name='nom')
    email = models.EmailField()
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='invité par')
    type = models.ForeignKey('Type', null=False, blank=False, verbose_name='type')
    created_at = models.DateTimeField(auto_now_add=True)
    max_seats = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Type(models.Model):
    class Meta:
        verbose_name = 'type'

    name = models.CharField(max_length=255, verbose_name='nom')

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'commande'

    yurplan_id = models.CharField(max_length=100, verbose_name='ID Yurplan')
    seats_count = models.IntegerField(verbose_name='nombre de places')
    guest = models.ForeignKey('Guest', null=False, blank=False)
