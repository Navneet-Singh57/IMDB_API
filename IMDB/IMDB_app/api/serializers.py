from rest_framework import serializers
from IMDB_app.models import Watchlist, StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['watchlist']

class WatchListSerializer(serializers.ModelSerializer):
    
    reviews = ReviewSerializer(many=True, read_only=True)
       
    class Meta:
        model = Watchlist
        fields = '__all__'
        read_only_fields = ['id']  
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[validate_name])
#     description = serializers.CharField(max_length=500)
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data) 
    
#     def update(self,instance, validated_data):
#         instance.name = validated_data.get('name','instance.name')
#         instance.description = validated_data.get('description','instance.description')
#         instance.active = validated_data.get('active','instance.active')
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Please give proper description.')
#         return data
        
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('Name is too short.')
    #     return value
    
    