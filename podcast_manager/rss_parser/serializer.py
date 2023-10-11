from rest_framework import serializers
from .models import ModelParser, Like

class ModelParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelParser
        fields = ('link','description','title')
        extra_kwargs = {
            'description':{'read_only':True},
            'title':{'read_only':True}
        }


class LikedPodcastsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'podcast')