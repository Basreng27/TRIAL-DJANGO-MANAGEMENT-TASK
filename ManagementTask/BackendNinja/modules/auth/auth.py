from django.contrib.auth import authenticate
from ManagementTask.helpers import response_json
from rest_framework import status
from datetime import datetime, timedelta
from jwt import encode
from django.conf import settings
from django.contrib.auth.models import User
from ...models import BlacklistedToken

def login_process(request, payload):
    try:
        username = payload.username
        password = payload.password
        
        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="Username or Password is Incorrect")
        
        expiration = datetime.utcnow() + timedelta(hours=3)
        token = encode({
            'user_id': user.id,
            'exp': expiration
        }, settings.SECRET_KEY, algorithm='HS256')
        
        data = {
            "token": token
        }
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except User.DoesNotExist:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="Username or Password is Incorrect")

def logout_process(request):
    token = request.headers.get("Authorization").split(" ")[1]
    BlacklistedToken.objects.create(token=token)
    
    return response_json(status=True, code=status.HTTP_200_OK, message="Success Logout")