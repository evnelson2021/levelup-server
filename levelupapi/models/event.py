from django.db import models
# from django.contrib.auth.models import User

# class Gamers(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.CharField(max_length=50)

class Event(models.Model):
    organizing_gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    # organizer = models.ManyToManyField(Gamers)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="games")
    location = models.CharField(max_length=150)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    details = models.CharField(max_length=350)
    attendees = models.ManyToManyField("Gamer", through="attendee", related_name="attendees")
