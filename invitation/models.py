# coding=utf-8
from django.db import models


class Guest(models.Model):
    class Meta:
        verbose_name = 'Invité'

    name = models.CharField(max_length=255, verbose_name='Nom')
    email = models.EmailField()
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Invité par')
    type = models.ForeignKey('Type', null=False, blank=False, verbose_name='Type')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    class Meta:
        verbose_name = 'Type'

    name = models.CharField(max_length=255, verbose_name='Nom')
    max_seats = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'Commande'

    yurplan_id = models.CharField(max_length=100, verbose_name='ID Yurplan')
    seats_count = models.IntegerField(verbose_name='Nombre de places')
    guest = models.ForeignKey('Guest', null=False, blank=False)