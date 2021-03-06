from __future__ import unicode_literals

from django.db import models
import os
import re
import config


# TODO Move this to separate functions file
def elo_change(player, elo2, score1, score2, k=32):
    s = 1 if score1 > score2 else 0 if score2 > score1 else 0.5
    e = 1 / (1 + 10 ** ((elo2-player.player_elo)/400))
    delta = k * (s - e)

    player.player_elo += delta
    player.save()

# Create your models here.
class TfPlayer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=2, default='AC')
    player_elo = models.IntegerField(default=config.DEFAULT_ELO)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name

class TfTeam(models.Model):
    players = models.ManyToManyField(TfPlayer)
    team_matches_played = models.IntegerField(default=0)
    team_matches_won = models.IntegerField(default=0)
    is_single_player = models.BooleanField(default=False)

    def team_elo(self):
        if self.is_single_player:
            return int(self.players.order_by('id')[0].player_elo)
        else:
            return int((self.players.order_by('id')[1].player_elo + self.players.order_by('id')[0].player_elo) / 2)

    def prettyprint(self):
        if self.is_single_player:
            s = str(self.players.order_by('id')[0])
        else:
            s = str(self.players.order_by('id')[0]) + ' / ' + str(self.players.order_by('id')[1])
        return s

    def __str__(self):
        s = ''
        for p in self.players.order_by('id'):
            s = s + str(p) + '\n'
        return s

class TfMatch(models.Model):
    class Meta:
        verbose_name_plural = "tf matches"

    teams = models.ManyToManyField(TfTeam)
    scores = models.CharField(max_length=5, default="0 0")

    played_date = models.DateTimeField('date played')
    invisible = models.BooleanField(default=False)

    def scores_to_int(self):
        match = re.search('(.)\s(.)', self.scores)
        score1 = int(match.group(1))
        score2 = int(match.group(2))
        return [score1, score2]

    def get_winner(self):
        [score1, score2] = self.scores_to_int()
        teams = self.teams.order_by('id').all()

        if score1 > score2:
            return teams[0]
        else:
            return teams[1]

    def get_loser(self):
        [score1, score2] = self.scores_to_int()
        teams = self.teams.order_by('id').all()

        if score1 > score2:
            return teams[1]
        else:
            return teams[0]

    def get_scores(self):
        [score1, score2] = self.scores_to_int()

        if score1 > score2:
            return str(score1) + '-' + str(score2)
        else:
            return str(score2) + '-' + str(score1)

    def update_elos(self, k=32, debug=False):

        winner = self.get_winner()
        loser = self.get_loser()

        if debug:
            print(str(self.played_date)[:16])

            print("Before")
            print("W: ", end='')
            print(str(winner.players.order_by('id')[0]) + ' (' + str(winner.players.order_by('id')[0].player_elo) + ')', end='')
            if not winner.is_single_player:
                print('/ ' + str(winner.players.order_by('id')[1]) + ' (' + str(winner.players.order_by('id')[1].player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(winner.team_elo())))

            print("L: ", end='')
            print(str(loser.players.order_by('id')[0]) + ' (' + str(loser.players.order_by('id')[0].player_elo) + ')', end='')
            if not loser.is_single_player:
                print('/ ' + str(loser.players.order_by('id')[1]) + ' (' + str(loser.players.order_by('id')[1].player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(loser.team_elo())))

        elo_winner = winner.team_elo()
        elo_loser = loser.team_elo()

        e = 1 / (1 + 10 ** ((elo_loser-elo_winner)/400))
        delta_winner = k * (1 - e)
        delta_loser = k * (0 - e)

        for p in winner.players.all():
            p.player_elo += delta_winner
            p.save()

        for p in loser.players.all():
            p.player_elo += delta_loser
            p.save()

        if debug:
            print("After")
            print("W: ", end='')
            print(str(winner.players.order_by('id')[0]) + ' (' + str(winner.players.order_by('id')[0].player_elo) + ')', end='')
            if not winner.is_single_player:
                print('/ ' + str(winner.players.order_by('id')[1]) + ' (' + str(winner.players.order_by('id')[1].player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(winner.team_elo())))

            print("L: ", end='')
            print(str(loser.players.order_by('id')[0]) + ' (' + str(loser.players.order_by('id')[0].player_elo) + ')', end='')
            if not loser.is_single_player:
                print('/ ' + str(loser.players.order_by('id')[1]) + ' (' + str(loser.players.order_by('id')[0].player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(loser.team_elo())))

            print('---')

    def __str__(self):
        [score1, score2] = self.scores_to_int()

        if score1 > score2:
            return  str(self.get_winner()) + ' ' + str(score1) + '-' \
               + str(score2) + ' ' + str(self.get_loser())
        else:
            return  str(self.get_winner()) + ' ' + str(score2) + '-' \
               + str(score1) + ' ' + str(self.get_loser())

    def prettyprint(self):
        [score1, score2] = self.scores_to_int()

        if score1 > score2:
            return  self.get_winner().prettyprint() + ' ' + str(score1) + '-' \
               + str(score2) + ' ' + self.get_loser().prettyprint()
        else:
            return  self.get_winner().prettyprint() + ' ' + str(score2) + '-' \
               + str(score1) + ' ' + self.get_loser().prettyprint()
