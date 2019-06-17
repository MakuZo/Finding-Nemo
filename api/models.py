from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """Class representing a genre"""
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Movie(models.Model):
    """Class representing a movie"""
    title = models.CharField(max_length=250)
    score = models.FloatField(validators=[MaxValueValidator(5.0), MinValueValidator(0.5)], null=True)
    genres = models.ManyToManyField(Genre)
    link = models.CharField(max_length=512)
    year = models.IntegerField(null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{self.title} ({self.year})".format(self=self)

class Tag(models.Model):
    """Class representing a tag"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.CharField(max_length=250)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.tag
