from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations", default=None)
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations", default=None)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.room} reservation made by {self.user} {self.start} ~ {self.end}"

