from django.shortcuts import render
from rest_framework.response import Response
from IMDB_app.models import Movie
from .serializers import MovieSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=200)
    else: 
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else: 
            return Response(serializer.errors, status=400)
    
    
@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except:
        return Response(status=404)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else: 
            return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=204)