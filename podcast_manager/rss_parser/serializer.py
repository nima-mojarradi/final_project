from rest_framework import serializers
from .models import EpisodeData, LikeEpisode, PodcastData, Subscription, LikePodcast, Comment, BookMark


class ModelParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeData
        fields = ('link','description','title')
        extra_kwargs = {
            'description':{'read_only':True},
            'title':{'read_only':True}
        }


class LikedPodcastsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    episode = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LikePodcast
        fields = ('user', 'podcast')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    episode = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ('user', 'episode')


class LikedEpisodeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    episode = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LikeEpisode
        fields = ('user', 'episode')


class BookMarkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    episode = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = BookMark
        fields = ('user', 'episode')

class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    podcast = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Subscription
        fields = ('user', 'podcast')

class ChannelSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = PodcastData
        fields = ['id', 'title', 'subscribed', 'description','last_update', 'language', 'subtitle',
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