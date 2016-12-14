# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0011_auto_20161124_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='email_received',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='guest',
            name='last_seen_at',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='dernière visite'),
        ),
    ]