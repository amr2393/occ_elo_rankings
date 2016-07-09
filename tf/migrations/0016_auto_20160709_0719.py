# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-09 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0015_auto_20160703_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfmatch',
            name='scores',
            field=models.CharField(default='0 0', max_length=5),
        ),
        migrations.AddField(
            model_name='tfmatch',
            name='teams',
            field=models.ManyToManyField(to='tf.TfTeam'),
        ),
    ]
