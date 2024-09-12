from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('interviewer', 'Interviewer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class TimeSlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.start_time} to {self.end_time})"
