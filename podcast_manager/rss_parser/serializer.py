from rest_framework import serializers
from .models import EpisodeData, LikeEpisode

class ModelParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeData
        fields = ('link','description','title')
        extra_kwargs = {
            'description':{'read_only':True},
            'title':{'read_only':True}
        }


class LikedPodcastsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeEpisode
        fields = ('id', 'user', 'podcast')