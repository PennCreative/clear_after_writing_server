from django.db import models
from .journal import Journal
from .survey import Survey


class Stat(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='journal_id')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='question_id')
    rating = models.PositiveIntegerField()
