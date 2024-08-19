from ninja import NinjaAPI
from ninja.security import HttpBearer
from .models import BlacklistedToken
from ManagementTask.helpers import response_json
from rest_framework import status
from jwt import decode as jwt_decode, exceptions
from django.conf import settings
from django.contrib.auth.models import User
from .modules.auth.auth import login_process, logout_process
from .modules.auth.schema import LoginSchema

api = NinjaAPI()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if BlacklistedToken.objects.filter(token=token).exists():
            return response_json(False, status.HTTP_401_UNAUTHORIZED, "Token Expired", None)
        
        try:
            decode = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            return User.objects.get(id=decode['user_id'])
        except (exceptions.DecodeError, User.DoesNotExist):
            return response_json(False, status.HTTP_401_UNAUTHORIZED, "User Not Exist", None)

auth = AuthBearer()

@api.post("/login")
def login(request, payload:LoginSchema):
    return login_process(request, payload)

@api.post("/logout")
def login(request):
    return logout_process(request)