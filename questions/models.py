# coding=utf-8

from django.db import models


class Question(models.Model):
    class Meta:
        verbose_name = 'question'

    TYPES = (
        ('T', 'Champ'),
        ('Z', 'Zone libre'),
        ('C', 'Case à cocher'),
        ('R', 'Boutton radio'),
    )

    question = models.CharField(max_length=511)
    description = models.TextField()
    type = models.CharField(max_length=1, default='T', choices=TYPES)
    data = models.TextField()


class Answer(models.Model):
    class Meta:
        verbose_name = 'réponse'

    data = models.TextField()
    question = models.ForeignKey('Question', related_name='réponses')

    def __str__(self):
        return self.name
