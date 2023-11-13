from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_events")
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    attendees = models.ManyToManyField(
        User, through="EventGamer", related_name="events")
