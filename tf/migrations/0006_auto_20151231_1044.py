# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0005_auto_20151231_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfplayer',
            name='score',
            field=models.IntegerField(default=800),
        ),
    ]
