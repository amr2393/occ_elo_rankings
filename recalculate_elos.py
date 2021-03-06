# exec(open("recalculate_elos.py").read(), globals())

import config
from tf import models

players = models.TfPlayer.objects.all()
for p in players:
    p.player_elo = config.DEFAULT_ELO
    p.save()

matches = models.TfMatch.objects.order_by('played_date').all()
for m in matches:
    m.update_elos(debug=True)
