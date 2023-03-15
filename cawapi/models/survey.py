from django.db import models
from .journal import Journal
class Survey(models.Model):
    question = models.CharField(max_length=255)
    answer = models.PositiveIntegerField()
