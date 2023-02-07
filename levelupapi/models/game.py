from django.db import models


class Game(models.Model):
    type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    length = models.FloatField()
    min_age = models.FloatField()
    min_players = models.FloatField()
    max_players = models.FloatField()
