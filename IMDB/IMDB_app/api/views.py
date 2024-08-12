from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from IMDB_app.models import Watchlist, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from django.http import JsonResponse  
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

# Create your views here.

class ReviewCreateAV(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)
        
        serializer.save(watchlist=watchlist)
        

class ReviewListAV(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# class ReviewDetailAV(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
        

# class ReviewListAV(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args,**kwargs)

class WatchListAV(APIView):
    
    def get(self, request):
        watchlist = Watchlist.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else: 
            return Response(serializer.errors, status=400)
        
class WatchDetailAV(APIView):
    
    def get(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else: 
            return Response(serializer.errors, status=400)
    
    def delete(self,request,pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except:
            return Response(status=404)
        watchlist.delete()
        return Response(status=204)
        
        
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)    
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         else: 
#             return Response(serializer.errors, status=400)
    
# class StreamPlatformListAV(APIView):
    
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         else: 
#             return Response(serializer.errors, status=400)
        
# class StreamPlatformDetailAV(APIView):
    
#     def get(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except:
#             return Response(status=404)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except:
#             return Response(status=404)
#         serializer = WatchListSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         else: 
#             return Response(serializer.errors, status=400)
    
#     def delete(self,request,pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except:
#             return Response(status=404)
#         platform.delete()
#         return Response(status=204)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data, status=200)
#     else: 
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         else: 
#             return Response(serializer.errors, status=400)
    
    
# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request,pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except:
#         return Response(status=404)
#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         else: 
#             return Response(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         movie.delete()
#         return Response(status=204)