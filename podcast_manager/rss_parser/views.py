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

class RequestUrl(APIView):
    def post(self, request):
        url = request.data.get('url')
        if url is None:
            return Response("no valid link")
        else:
            ParseChannel(url=url)
            return Response(status=status.HTTP_201_CREATED)
        

class LikeView(generics.GenericAPIView):
    # authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]
    # serializer_class = LikedEpisodeSerializer
    def get_object(self):
        return LikeEpisode.objects.create(user=self.request.user, podcast=self.args)

    def post(self, request, *args, **kwargs):
        like = self.get_object()
        if like:
            like.delete()
            return Response({"message": "Disliked successfully"}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data={'user': request.user.id, 'podcast': self.kwargs['user_id']})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Liked successfully"}, status=status.HTTP_20)

class CommentView(APIView):
    pass
    
class BookMarkView(APIView):
    pass


class RecommendationRetrieveView(APIView):
    pass