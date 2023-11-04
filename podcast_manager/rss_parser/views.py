from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .parser import ParseChannel
from .models import LikeEpisode, LikePodcast, Comment, BookMark, Recommendation, PodcastData, EpisodeData, Notification
from user.models import CustomUser
from user.authentication import Authentication
from .serializer import LikedEpisodeSerializer
from .serializer import ChannelSerializer, LikedEpisodeSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from user.publisher import publisher
from django.utils.translation import gettext_lazy as _
from config.mixins import LoggingMixin
from user.authentication import Authentication
import logging

class RequestUrl(LoggingMixin,APIView):
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
        

class LikeView(LoggingMixin,APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedEpisodeSerializer
    # logger = logging.getLogger(__name__)

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
            msg = {'status': _('Unliked!')}
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except LikeEpisode.DoesNotExist:
            msg = {'status': _('This episode is not liked!')}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

class CommentView(LoggingMixin,APIView):
    def post(self, request):
        user = request.user
        context = request.context
        podcast = request.podcast
        comment=Comment.objects.create(user=user, context=context, podcast=podcast)
        return comment

    
class BookMarkView(LoggingMixin,APIView):
    def post(self, request):
        bookmark = BookMark.objects.create(user=request.user, episode=request.args)
        return bookmark


class RecommendationRetrieveView(LoggingMixin,APIView):
    pass