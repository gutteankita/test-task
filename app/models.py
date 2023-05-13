from django.db import models

# Create your models here.


class Movie(models.Model):
    tconst = models.CharField(max_length=10, primary_key=True)
    titleType = models.CharField(max_length=20)
    primaryTitle = models.CharField(max_length=255)
    runtimeMinutes = models.IntegerField(null=True)
    genres = models.CharField(max_length=255)
    

    

class Rating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, primary_key=True)
    averageRating = models.DecimalField(max_digits=3, decimal_places=1)
    numVotes = models.IntegerField()

    
