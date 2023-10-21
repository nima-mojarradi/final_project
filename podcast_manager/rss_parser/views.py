from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .parser import ParseChannel
from .models import LikeEpisode, LikePodcast, Comment, BookMark, Recommendation, PodcastData
from .serializer import ChannelSerializer

class RequestUrl(APIView):
    def post(self, request):
        url = request.data.get('url')
        if url is None:
            return Response("no valid link")
        else:
            ParseChannel(url=url)
            return Response(status=status.HTTP_201_CREATED)
        

class LikeView(APIView):
    model = [LikePodcast, LikeEpisode]
            


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('context')
        return self.create_object(request, Comment, content=content)
    
class BookMarkView(APIView):
    model = BookMark


class RecommendationRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendation = Recommendation.objects.filter(user=request.user).order_by('-count').first()

        if recommendation:
            channels = PodcastData.objects.filter(category=recommendation.category)[:5]
            serializer = ChannelSerializer(channels, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No recommendations available for this user."}, status=status.HTTP_404_NOT_FOUND)