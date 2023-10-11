import jwt
import datetime
from rest_framework import exceptions

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
