# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0003_auto_20161123_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]