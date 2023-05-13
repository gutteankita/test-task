from django.urls import path
from .views import upload_csv, high_rated_movies,  update_runtime_minutes
from app import views


urlpatterns = [
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('top-rated-movies/', high_rated_movies, name='high_rated_movies'),
    # path('genre_movies_with_subtotals/', genre_movies_with_subtotals, name='genre_movies_with_subtotals'),
    path('update_runtime_minutes/', update_runtime_minutes, name='update_runtime_minutes'),

    path('movies/', views.MovieRatingView.as_view()),
]
