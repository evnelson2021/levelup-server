from django.db import models


class Event(models.Model):
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    date = models.CharField(max_length=50)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    details = models.CharField(max_length=350)