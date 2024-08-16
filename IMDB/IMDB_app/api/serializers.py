from rest_framework import serializers
from IMDB_app.models import Watchlist, StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ['watchlist']

class WatchListSerializer(serializers.ModelSerializer):
    
    # reviews = ReviewSerializer(many=True, read_only=True)
    
    platform = serializers.CharField(source='platform.name')  
       
    class Meta:
        model = Watchlist
        fields = '__all__'
        read_only_fields = ['id']  
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'