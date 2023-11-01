from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .parser import ParseChannel
from .models import LikeEpisode, LikePodcast, Comment, BookMark, Recommendation, PodcastData, EpisodeData
from user.models import CustomUser
from user.authentication import Authentication
from .serializer import LikedEpisodeSerializer
from .serializer import ChannelSerializer, LikedEpisodeSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from user.publisher import publisher
from django.utils.translation import gettext_lazy as _

class RequestUrl(APIView):
    def post(self, request):
        url = request.data.get('url')
        if url is None:
            publisher('update_invalid_podcast', "the url you requested is invalid")
            return Response("no valid link")
        else:
            ParseChannel(url=url)
            publisher('update_valid_podcast', 'all episodes of the requested podcasts updated for you')
            return Response(status=status.HTTP_201_CREATED)
        

class LikeView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedEpisodeSerializer
    def post(self, request, *args, **kwargs):
        print(request.user)
        print("*"*100)
        # episode = get_object_or_404(EpisodeData, id=request.data.get('episode'))
        like = LikeEpisode.objects.filter(user=request.user, episode_id=request.data.get('episode'))
        if like:
            like.get().delete()
            return Response({_("message"): _("Disliked successfully")}, status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data={'user': request.user.id, 'episode': request.data.get('episode')})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({_("message"): _("Liked successfully")}, status=status.HTTP_200_OK)

class CommentView(APIView):
    pass
    
class BookMarkView(APIView):
    def post(self, request):
        bookmark = BookMark.objects.create(user=self.request.user, episode=self.args)
        return bookmark


class RecommendationRetrieveView(APIView):
    pass