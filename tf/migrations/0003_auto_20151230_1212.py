# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0002_auto_20151230_1205'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TFMatch',
            new_name='TF_Match',
        ),
        migrations.RenameModel(
            old_name='TFPlayer',
            new_name='TF_Player',
        ),
        migrations.RenameModel(
            old_name='TFTeam',
            new_name='TF_Team',
        ),
    ]
