from django.shortcuts import render
from django.views.decorators.http import require_safe
from rest_framework.response import Response
from .models import Movie
import random

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)



@require_safe
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {
        'movie': movie
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request, movie_pk):
    movies = Movie.objects.all()
    
    movie = Movie.objects.get(pk=movie_pk)
    genres = movie.genres.all()
    original_genres_lst = []
    for i in range(len(genres)):
        original_genres_lst.append(genres[i].pk)
    # print(genres_lst)
    # genres_lst.sort()

    every_movie_genres = []
    for j in range(100):
        movie_genre_lst = []
        genres2 = movies[j].genres.all()
        for k in range(len(genres2)):
            movie_genre_lst.append(genres2[k].pk)
        # 전체 영화의 장르 id를 담은 리스트
        every_movie_genres.append([j + 1, movie_genre_lst, movies[j].vote_average])

    # print(every_movie_genres)
    recommended_lst = []
    for genre in every_movie_genres:
        cnt = 0
        for id in original_genres_lst:
            if id in genre[1]:
                cnt += 1
        if cnt >= len(original_genres_lst) // 2 and genre[2] >= 8.5:
            recommended_lst.append(genre[0])
    if len(recommended_lst) < 10:
        random_recommended_lst = recommended_lst
    else:
        random_recommended_lst = random.sample(recommended_lst, 10)
    # print(random_recommended_lst)
    context = {
        'movies' : movies,
        'random_recommended_lst' : random_recommended_lst,
    }
    return render(request, 'movies/recommended.html', context)
    
    
