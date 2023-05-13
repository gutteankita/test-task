from django.shortcuts import render
import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from rest_framework import status
from django.http import JsonResponse
import json
from django.db.models import Avg
from django.db import connection
from django.http import JsonResponse

# Create your views here.


@api_view(['POST'])
def upload_csv(request):
    file_path = 'C:/Users/Ankita Patil/Downloads/movies.csv'
    movies_csv_file = open(file_path, 'r', encoding='utf-8-sig')
    decoded_movies_file = movies_csv_file.read().splitlines()
    movies_reader = csv.reader(decoded_movies_file)
    next(movies_reader)  # skip header row

    file_path = 'C:/Users/Ankita Patil/Downloads/ratings.csv'
    ratings_csv_file = open(file_path, 'r', encoding='utf-8-sig')
    decoded_ratings_file = ratings_csv_file.read().splitlines()
    ratings_reader = csv.reader(decoded_ratings_file)
    next(ratings_reader)  # skip header row

    for row in movies_reader:
        tconst, titleType, primaryTitle, runtimeMinutes, genres = row[0], row[1], row[2], row[3], row[4]
        try:
            movie = Movie.objects.get(tconst=tconst)
            movie.titleType = titleType
            movie.primaryTitle = primaryTitle
            movie.runtimeMinutes = runtimeMinutes
            movie.genres = genres
            movie.save()
        except Movie.DoesNotExist:
            movie = Movie.objects.create(tconst=tconst, titleType=titleType, primaryTitle=primaryTitle, runtimeMinutes=runtimeMinutes, genres=genres)
            movie.save()
            print(f"Created movie with tconst {tconst}")
        


    for row in ratings_reader:
        tconst, averageRating, numVotes = row[0], row[1], row[2]
        movie = Movie.objects.get(tconst=tconst)
        rating, created = Rating.objects.get_or_create(movie=movie, defaults={'averageRating': averageRating, 'numVotes': numVotes})
        if not created:
            rating.averageRating = averageRating
            rating.numVotes = numVotes
            rating.save()

    return Response({'message': 'CSV data uploaded successfully.'})


@api_view(['GET'])
def high_rated_movies(request):
    high_rated = Movie.objects.annotate(avg_rating=Avg('rating__averageRating')).filter(avg_rating__gt=6.0).order_by('-avg_rating')

    movie_list = []
    for movie in high_rated:
        movie_dict = {
            'tconst': movie.tconst,
            'primaryTitle': movie.primaryTitle,
            'genre': movie.genres,
            'averageRating': round(movie.avg_rating, 2)
        }
        movie_list.append(movie_dict)

    return Response({'movies': movie_list})




class MovieRatingView(APIView):

    def get(self, request):
        try:
            top_movies = Movie.objects.order_by('-runtimeMinutes')[:10]
            movies_data = []
            for movie in top_movies:
                movie_data = {
                    'tconst': movie.tconst,
                    'primaryTitle': movie.primaryTitle,
                    'runtimeMinutes': movie.runtimeMinutes,
                    'genres': movie.genres,
                }
                movies_data.append(movie_data)
            return Response({'movies': movies_data})
        except Exception as e:
            error = {'error': str(e)}
            return Response(error, status=500)
        
    def post(self, request):
        try:
            data = json.loads(request.body)
            movie = Movie(
                tconst=data.get('tconst'),
                titleType=data.get('titleType'),
                primaryTitle=data.get('primaryTitle'),
                runtimeMinutes=data.get('runtimeMinutes'),
                genres=data.get('genres')
            )
            movie.save()
            return Response({'message': 'success'})
        except Exception as e:
            return Response({'message': str(e)})





def update_runtime_minutes(request):
    # execute the SQL query to update the runtimeMinutes field
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE app_movie
            SET runtimeMinutes = CASE
                WHEN genres = 'Documentary' THEN runtimeMinutes - 15
                WHEN genres = 'Animation' THEN runtimeMinutes - 30
                ELSE runtimeMinutes - 45
            END
        """)

    # return a JSON response indicating success
    return JsonResponse({'status': 'success'})

