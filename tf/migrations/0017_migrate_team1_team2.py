# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-09 06:20
from __future__ import unicode_literals

from django.db import migrations

def migrate_teams(apps, schema_editor):
    Matches = apps.get_model("tf", "TfMatch")
    for m in Matches.objects.all():

        if m.team1.id < m.team2.id:
            m.teams.add(m.team1, m.team2)
            m.scores = str(m.score1) + ' ' + str(m.score2)
        else:
            m.teams.add(m.team2, m.team1)
            m.scores = str(m.score2) + ' ' + str(m.score1)

        m.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0016_auto_20160709_0719'),
    ]

    operations = [
        migrations.RunPython(migrate_teams)
    ]
