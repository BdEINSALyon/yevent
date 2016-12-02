# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_auto_20161201_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='allowed_options',
            field=models.ManyToManyField(blank=True, related_name='allowed_prices', to='ticketing.OptionPrice', verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='optionprice',
            name='prices',
            field=models.ManyToManyField(blank=True, related_name='questionable_options', to='ticketing.Price', verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='price',
            name='required_questions',
            field=models.ManyToManyField(blank=True, related_name='questionable_prices', to='questions.Question', verbose_name='questions'),
        ),
    ]