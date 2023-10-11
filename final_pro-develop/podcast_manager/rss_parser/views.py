from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import LikedPodcastsSerializer
from .models import Like, ModelParser


class LikedPodcasts(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        likes = Like.objects.filter(user=request.user)
        podcast_ids = [like.title.id for like in likes]
        podcasts = ModelParser.objects.filter(id__in=podcast_ids)
        podcast_categories = [podcast.category for podcast in podcasts]
        suggested_podcasts = ModelParser.objects.filter(category__in=podcast_categories).exclude(id__in=podcast_ids)
        serializer = LikedPodcastsSerializer(suggested_podcasts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

