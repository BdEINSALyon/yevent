# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-14 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invitation', '0015_auto_20170114_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
                ('maximum_registration_by_guest', models.IntegerField(default=7)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, verbose_name='nombre')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('used', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invitation.Guest', verbose_name='propriétaire')),
                ('waiting_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waitlist.WaitingList')),
            ],
            options={
                'verbose_name': "Ticket d'attente",
            },
        ),
    ]