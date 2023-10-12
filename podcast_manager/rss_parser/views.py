from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .parser import ParseChannel

class RequestUrl(APIView):
    def post(self, request):
        url = request.data.get('url')
        if url is None:
            return Response("no valid link")
        else:
            ParseChannel(url=url)
            return Response(status=status.HTTP_201_CREATED)
            

