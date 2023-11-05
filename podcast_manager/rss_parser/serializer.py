from rest_framework import serializers
from .models import EpisodeData, LikeEpisode, PodcastData, Subscription, LikePodcast, Comment, BookMark
from django.utils.translation import gettext_lazy as _


class ModelParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeData
        fields = (_('link'),_('description'),_('title'))
        extra_kwargs = {
            'description':{'read_only':True},
            'title':{'read_only':True}
        }


class LikedPodcastsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    episode = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LikePodcast
        fields = (_('user'), _('podcast'))


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
        fields = (_('user'), _('episode'))


class BookMarkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    episode = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = BookMark
        fields = (_('user'), _('episode'))

class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    podcast = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Subscription
        fields = (_('user'), _('podcast'))

class ChannelSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = PodcastData
        fields = [_('id'), _('title'), _('subscribed'), _('description'),_( 'last_update'), _('language'), _('subtitle'),
                  _('image'), _('author'), _('xml_link'), _('category'), _('owner')]
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