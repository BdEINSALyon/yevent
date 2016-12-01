# coding=utf-8

from django.db import models
from questions.models import Answer, Question


class Ticket(models.Model):
    class Meta:
        verbose_name = 'billet'
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    price = models.ForeignKey('Price', related_name='tickets', verbose_name='tarif')
    options = models.ManyToManyField('OptionPrice', related_name='tickets', verbose_name='tarif')
    answers = models.ManyToManyField('questions.Answer', related_name='tickets', verbose_name='réponses')


class Saleable(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, verbose_name='nom')
    price = models.FloatField(default=0)
    description = models.TextField(blank=True)
    vat = models.FloatField(default=0.20)
    limit = models.IntegerField()

    def __str__(self):
        return self.name


class Price(Saleable):
    class Meta:
        verbose_name = 'tarif'

    required_questions = models.ManyToManyField('questions.Question', related_name='questionable_prices',
                                                verbose_name='questions', blank=True)
    allowed_options = models.ManyToManyField('OptionPrice', related_name='allowed_prices',
                                             verbose_name='options', blank=True)


class OptionPrice(Saleable):
    class Meta:
        verbose_name = 'option tarifaire'

    prices = models.ManyToManyField('Price', related_name='questionable_options', verbose_name='options', blank=True)
    multiple = models.BooleanField(default=False)