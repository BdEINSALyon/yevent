# coding=utf-8

from django.db import models


class Question(models.Model):
    class Meta:
        verbose_name = 'question'

    TYPES = (
        ('T', 'Champ'),
        ('Z', 'Zone libre'),
        ('R', 'Boutton radio'),
    )

    question = models.CharField(max_length=511)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=1, default='T', choices=TYPES)
    data = models.TextField(blank=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    class Meta:
        verbose_name = 'réponse'

    data = models.TextField(blank=True)
    question = models.ForeignKey('Question', related_name='réponses')
