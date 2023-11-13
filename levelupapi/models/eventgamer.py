from django.db import models
from django.contrib.auth.models import User


class EventGamer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="signed_up_events"
    )
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="participants")
