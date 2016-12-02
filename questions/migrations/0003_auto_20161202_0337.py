# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20161201_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('T', 'Champ'), ('Z', 'Zone libre'), ('R', 'Boutton radio')], default='T', max_length=1),
        ),
    ]