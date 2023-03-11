from django.db import models
from .user import User

class Journal(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    goal_entry = models.CharField(max_length=500)
    affirmation = models.CharField(max_length=255)
    distraction = models.CharField(max_length=255)
    entry = models.CharField(max_length=1000)
    significant = models.BooleanField(default=False)
    overall_rating = models.FloatField(default=0, null=True)
