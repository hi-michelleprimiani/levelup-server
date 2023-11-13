from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_games"
    )
    name = models.CharField(max_length=100)
    gametype = models.ForeignKey(
        "GameType", on_delete=models.CASCADE, related_name="games")
    description = models.CharField(max_length=260)
    difficulty = models.IntegerField()
    duration = models.DecimalField(decimal_places=2, max_digits=4)
    num_of_players = models.IntegerField()
