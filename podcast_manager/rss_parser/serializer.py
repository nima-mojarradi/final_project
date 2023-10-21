from rest_framework import serializers
from .models import EpisodeData, LikeEpisode, PodcastData, Subscription

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




class ChannelSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = PodcastData
        fields = ['id', 'title', 'subscribed', 'description', 'last_update', 'language', 'subtitle',
                  'image', 'author', 'xml_link', 'category', 'owner']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                channel=obj,
                user=user
            ).exists()
        return False