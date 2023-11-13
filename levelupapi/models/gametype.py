from django.db import models


class GameType(models.Model):
    description = models.CharField(max_length=100)
