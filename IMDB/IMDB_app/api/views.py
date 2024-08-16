from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from IMDB_app.models import Watchlist, StreamPlatform, Review
from django.http import JsonResponse  
from rest_framework import generics, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle, UserRateThrottle
from . import pagination, permissions, serializers, throttling

# Create your views here.

class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreateAV(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)
        
        reviewer = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, reviewer=reviewer)
        
        if review_queryset.exists():
            raise ValidationError('Review already exists')
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else: 
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.number_rating = watchlist.number_rating+1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, reviewer=reviewer)
        

class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','reviewer__username']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserorReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'


class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request):
        watchlist = Watchlist.objects.all()
        serializer = serializers.WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else: 
            return Response(serializer.errors, status=400)
        
class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = serializers.WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = serializers.WatchListSerializer(watchlist, data=request.data)
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
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    

class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = serializers.StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = serializers.WatchListSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else: 
            return Response(serializer.errors, status=400)
    
    def delete(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=404)
        platform.delete()
        return Response(status=204)

