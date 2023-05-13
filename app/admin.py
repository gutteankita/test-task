from django.contrib import admin
from app.models import *

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['tconst', 'titleType', 'primaryTitle', 'runtimeMinutes', 'genres']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'averageRating', 'numVotes']
