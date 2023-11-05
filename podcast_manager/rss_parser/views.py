from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .parser import ParseChannel
from .models import LikeEpisode, LikePodcast, Comment, BookMark, Recommendation, PodcastData, EpisodeData, Notification, Subscription
from user.models import CustomUser
from user.authentication import Authentication
from .serializer import LikedEpisodeSerializer
from .serializer import ChannelSerializer, LikedEpisodeSerializer, CommentSerializer, SubscribeSerializer, BookMarkSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from user.publisher import publisher
from django.utils.translation import gettext_lazy as _
from user.authentication import Authentication
from .tasks import parse_rss_links
import json
import logging

class RequestUrl(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [Authentication]
    def post(self, request):
        url = request.data.get('url')
        user = request.user
        if not url:
            parse_rss_links.delay()
            publisher('update_invalid_podcast',{'user_id':request.user.id, 'massage':'podcast you wanted updated'})
            return Response("all links updated")
        else:
            ParseChannel(url=url)
            publisher('update_valid_podcast' ,{'user_id':request.user.id, 'massage':'all episodes of the requested podcasts updated for you'})
            return Response(status=status.HTTP_201_CREATED)
        

class AllPodcasts(APIView):
    def post(self,request):
        podcasts = PodcastData.objects.all().values()
        return Response(json.dumps(list(podcasts)))
        

class LikeView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedEpisodeSerializer

    def post(self, request, episode_id):
        episode = EpisodeData.objects.get(id=episode_id)
        try:
            like = LikeEpisode.objects.get(user=request.user, episode=episode)
            msg = {'status': _('This episode is already liked!')}
            return Response(msg, status=status.HTTP_200_OK)
        except LikeEpisode.DoesNotExist:
            like = LikeEpisode.objects.create(user=request.user, episode=episode)
            serializer = self.serializer_class(like)
            msg = {'status':'episode liked successfuly'}
            return Response(msg, status=status.HTTP_201_CREATED)

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

class AllCommentsOnEpisode(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    def post(self, request, episode_id):
        comments = Comment.objects.filter(podcast_id = episode_id).values()
        all_comments = list(comments)
        return Response(all_comments)

class CountOfLikes(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    def post(self,request, episode_id):
        like_count = LikeEpisode.objects.filter(episode_id=episode_id).count()
        return Response({'count_of_likes':like_count})
            
class BookMarkView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookMarkSerializer
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
    serializer_class = LikedEpisodeSerializer
    def post(self,request):
        liked_episodes = LikeEpisode.objects.filter(user=request.user).values()
        return Response(json.dumps(list(liked_episodes)))
        
class AllBookmarkedPodcasts(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookMarkSerializer
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
