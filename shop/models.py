# coding=utf-8

from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = 'commande'
    STATUSES = (
        ('ONGOING', 'En cours'),
        ('QUESTIONS', 'Remplis les questions'),
        ('PAYMENT', 'En cours de paiement'),
        ('WAITING_PAYMENT', 'En attente du paiement'),
        ('PAID', 'Payé'),
    )
    status = models.CharField(verbose_name='statut', choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    promotion = models.ForeignKey(
        'PromoCode',
        null=True,
        blank=True,
        related_name='orders'
    )


class PromoCode(models.Model):
    class Meta:
        verbose_name = 'code de réduction'

    name = models.CharField(max_length=255, verbose_name='nom')
    code = models.CharField(max_length=255, verbose_name='code')
    amount_off = models.FloatField(default=0)
    percent_off = models.FloatField(default=0)

    def __str__(self):
        return self.name