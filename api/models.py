from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Genre(models.Model):
    """Class representing a movie genre"""
    name = models.CharField(max_length=120)

class Movie(models.Model):
    """Class representing a movie"""
    title = models.CharField(max_length=250)
    score = models.FloatField()
    genres = models.ManyToManyField(Genre)
    link = models.CharField(max_length=512)
    year = models.IntegerField()
