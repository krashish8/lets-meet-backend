from django.db import models
from django.contrib.auth.models import User
import datetime

class Meetup(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    minutes = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetups')
    members = models.ManyToManyField(User, related_name='participating_meetups')
    zoom_link = models.URLField(blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    is_slack = models.BooleanField(default=False)
    date_and_time = models.DateTimeField(default=datetime.datetime.now())
    duration = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} - {self.date_and_time}'


class Response(models.Model):
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE, related_name='responses')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    response = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.meetup} - {self.member}'

class Task(models.Model):
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    