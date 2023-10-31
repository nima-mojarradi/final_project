import jwt
import datetime
from rest_framework import exceptions
from .models import CustomUser
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate as auth_authenticate
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
class Authentication(authentication.BaseAuthentication):
    def create_access_token(self,id, jti):
        """Create an access token for the given user."""
        return jwt.encode({
            'jti':jti,
            'user_id':id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow()
        }, 'access_secret', algorithm='HS256')


    def decode_access_token(self,token):
        try:
            payload = jwt.decode(token, 'access_secret', algorithms='HS256')
            return payload
        
        except:
            print('2'*100)


    def create_refresh_token(self,id, jti):
        """Create an access token for the given user."""
        return jwt.encode({
            'jti':jti,
            'user_id':id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow()
        }, 'refresh_secret', algorithm='HS256')

    def decode_refresh_token(self,token):
        try:
            payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')

            return payload
        
        except:
            print('1'*100)


    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        if not access_token:
            raise AuthenticationFailed(_('Access token not provided'))
        # try:
        payload = self.decode_access_token(access_token)
        if not payload:
            raise AuthenticationFailed(_('invalid access token'))
        user_id = self.verify_jti(payload)
        user = CustomUser.objects.filter(id=user_id)
        if not user:
            raise AuthenticationFailed(_('user not found'))
        print(user)
        print('2'*100)
        return user.first(),payload
        # except Exception as e:
        #     print(e)
        #     print('1'*100)
        #     raise AuthenticationFailed('Invalid access token!!!!!!!!!!')
        
    def verify_jti(self, payload):
        jti = payload.get('jti')
        token=cache.get(jti)
        if not token:
            raise AuthenticationFailed(_('token not found'))
        decode_token=self.decode_refresh_token(token=token)
        user_id=decode_token['user_id']
        if not user_id:
            raise AuthenticationFailed(_('user_id not in token'))
        else:
            return user_id

