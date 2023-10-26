from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from .authentication import Authentication
from rest_framework.exceptions import APIException
from .models import CustomUser
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from uuid import uuid4
from django.conf import settings
from django.core.cache import cache
from .publisher import publisher
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publisher('register', 'user registered')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginUserView(CreateAPIView):
    serializer_class = UserSerializer
    def post(self,request):
        user = CustomUser.objects.filter(username=request.data['username']).first()
        if not user:
            raise APIException('invalid credential')
        
        if not user.check_password(request.data['password']):
            raise APIException('invalid credential!')  

        jti = uuid4().hex      
        access_token = Authentication.create_access_token(user.id, jti)
        refresh_token = Authentication.create_refresh_token(user.id, jti)
        cache.set(jti, user.id)
        response = Response()
        response.set_cookie(key='refresh_token',value=refresh_token, httponly=True)
        response.data = {
            'access_token':access_token
        }
        publisher('login', 'user logged in')
        return response
    
    
class UserAPIView(APIView):
    def get(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = Authentication.decode_access_token(token)

            user = CustomUser.objects.filter(pk=id).first()

            return Response(UserSerializer(user).data)
        else:
            return Response("user is not authenticated")


