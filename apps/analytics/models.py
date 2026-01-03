from django.db import models
from apps.recepten.models import Recept

class DailyVisit(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} – {self.count}"

class ReceptViewCount(models.Model):
    recept = models.OneToOneField(
        "recepten.Recept",
        on_delete=models.CASCADE,
        related_name="view_count"
    )
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.recept.naam}: {self.count}"

