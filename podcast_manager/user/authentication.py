import jwt
import datetime
from rest_framework import exceptions
from .models import CustomUser
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate as auth_authenticate
class Authentication(authentication.BaseAuthentication):
    def create_access_token(id, jti):
        """Create an access token for the given user."""
        return jwt.encode({
            'jti':jti,
            'user_id':id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow()
        }, 'access_secret', algorithm='HS256')


    def decode_access_token(token):
        try:
            payload = jwt.decode(token, 'access_secret', algorithms='HS256')
            return payload['user_id']
        
        except:
            print('2'*100)


    def create_refresh_token(id, jti):
        """Create an access token for the given user."""
        return jwt.encode({
            'jti':jti,
            'user_id':id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow()
        }, 'refresh_secret', algorithm='HS256')

    def decode_refresh_token(token):
        try:
            payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')

            return payload['user_id']
        
        except:
            print('1'*100)


    def authenticate(self, request):
        access_token = request.headers.get('Authorization')
        if not access_token:
            raise AuthenticationFailed('Access token not provided')
        try:
            user = auth_authenticate(token=access_token)
            if user is None:
                raise AuthenticationFailed('Invalid access token')
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed('Invalid access token')
