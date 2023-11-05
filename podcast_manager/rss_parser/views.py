from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .parser import ParseChannel
from .models import LikeEpisode, LikePodcast, Comment, BookMark, Recommendation, PodcastData, EpisodeData, Notification, Subscription
from user.models import CustomUser
from user.authentication import Authentication
from .serializer import LikedEpisodeSerializer
from .serializer import ChannelSerializer, LikedEpisodeSerializer, CommentSerializer, SubscribeSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from user.publisher import publisher
from django.utils.translation import gettext_lazy as _
from user.authentication import Authentication
import json
import logging

class RequestUrl(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [Authentication]
    def post(self, request):
        url = request.data.get('url')
        user = request.user
        if url is None:
            publisher('update_invalid_podcast', "the url you requested is invalid")
            Notification.objects.create(user=request.user, notif_type='request_to_url', message='the url you requested was invalid')
            return Response("no valid link")
        else:
            ParseChannel(url=url)
            publisher('update_valid_podcast', 'all episodes of the requested podcasts updated for you')
            Notification.objects.create(user=request.user, notif_type='request_to_url', message='the url you requested was valid')
            return Response(status=status.HTTP_201_CREATED)
        

class AllPodcasts(APIView):
    def post(self,request):
        podcasts = PodcastData.objects.all().values()
        return Response(json.dumps(list(podcasts)))
        

class LikeView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedEpisodeSerializer
    # logger = logging.getLogger(__name__)

    def get(self,request):
        podcasts = LikeEpisode.objects.all().values()
        return Response(json.dumps(list(podcasts)))

    def post(self, request, episode_id):
        episode = EpisodeData.objects.get(id=episode_id)
        like = LikeEpisode.objects.get_or_create(user=request.user, episode=episode)

        if like:
            serializer = self.serializer_class(like)
            massage = {'status':'episode liked successfuly'}
            return Response(massage, status=status.HTTP_201_CREATED)
        else:
            msg = {'status': _('This episode is already liked!')}
            return Response(msg, status=status.HTTP_200_OK)
        
    
    def delete(self, request, episode_id):
        episode = EpisodeData.objects.get(id=episode_id)
        try:
            like = LikeEpisode.objects.get(user=request.user, episode=episode)
            like.delete()
            msg = {'status': 'Unliked!'}
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except LikeEpisode.DoesNotExist:
            msg = {'status':'This episode is not liked!'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

class CommentView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, podcast_id):
        podcast = EpisodeData.objects.get(id=podcast_id)
        comment = Comment.objects.create(user=request.user, podcast=podcast, context=request.data['context'])

        if comment:
            serializer = self.serializer_class(comment)
            massage = {'status': 'Comment added successfuly'}
            return Response(massage, status=status.HTTP_201_CREATED)
        else:
            msg = {'status': _('Unable to add comment!')}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            comment.delete()
            msg = {'status': 'Comment deleted!'}
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            msg = {'status': 'This comment does not exist or does not belong to the user!'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)


    
class BookMarkView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    def post(self, request, episode_id):
        try:
            episode = EpisodeData.objects.get(id=episode_id)
            bookmark = BookMark.objects.create(user=request.user, episode=episode)
            return Response(f'the episode with id {episode_id} bookmarked')
        except Exception as e:
            return Response('the episode that you want to bookmark is already in bookmarks')
    def delete(self, request, episode_id):
        try:
            episode=BookMark.objects.get(episode_id=episode_id)
            episode.delete()
            return Response('the episode you wanted deleted from the bookmarks')
        except Exception as e:
            return Response('something went wrong in your request')
        

class AllLikedPodcasts(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    def post(self,request):
        liked_episodes = LikeEpisode.objects.filter(user=request.user).values()
        return Response(json.dumps(list(liked_episodes)))
        
class AllBookmarkedPodcasts(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    def post(self,request):
        bookmarks = BookMark.objects.filter(user=request.user).values()
        return Response(json.dumps(list(bookmarks)))
        

class SubscribeView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer
    def post(self, request, channel_id):
        try:
            channel = PodcastData.objects.get(id=channel_id)
            subscription = Subscription.objects.create(user=request.user, channel=channel)
            return Response(f'the channel with id {channel_id} subscribed')
        except Exception as e:
            return Response('the episode that you want to bookmark is already in bookmarks')
    def delete(self, request, channel_id):
        try:
            channel=Subscription.objects.get(channel_id=channel_id)
            channel.delete()
            return Response(f'you unfollowed the channel with channel id {channel_id}')
        except Exception as e:
            return Response('something went wrong in your request')
