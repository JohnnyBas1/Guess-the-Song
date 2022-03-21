from django.db import models
import string
import random

# Create your models here.


# def get_average(song_id):

#     if Percent.song_id.filter(code=song_id):
#         pass  # Need to find out how to associate song_id with people and guessed correctly
#     pass


class Percent(models.Model):
    song_id = models.CharField(
        max_length=50, default="", unique=True, primary_key=True)
    people = models.IntegerField(null=False, default=0)
    guessed_correctly = models.IntegerField(null=False, default=0)
