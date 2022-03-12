from pyexpat import model
from django.db import models

class Playlist(models.Model):
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.url

class Video(models.Model):
    title = models.CharField(max_length=100)
    channel = models.CharField(max_length=50, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title