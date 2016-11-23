# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='max_seats',
        ),
        migrations.AddField(
            model_name='guest',
            name='max_seats',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='guest',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invitation.Guest', verbose_name='Invité par'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invitation.Type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='order',
            name='seats_count',
            field=models.IntegerField(verbose_name='Nombre de places'),
        ),
        migrations.AlterField(
            model_name='order',
            name='yurplan_id',
            field=models.CharField(max_length=100, verbose_name='ID Yurplan'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nom'),
        ),
    ]