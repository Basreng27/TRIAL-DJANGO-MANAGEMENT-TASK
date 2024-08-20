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
from .modules.projects.project import project_list, project_store, project_delete
from .modules.projects.schema import ProjectSchema

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

# Auth
@api.post("/login")
def login(request, payload:LoginSchema):
    return login_process(request, payload)

@api.post("/logout")
def login(request):
    return logout_process(request)

# Project
@api.get("/project", auth=auth)
def get_list(request):
    return project_list(request)

@api.get("/project/{id}", auth=auth)
def get(request, id: int):
    return project_list(request, id=id)

@api.post("/project", auth=auth)
def create(request, payload:ProjectSchema):
    return project_store(request, payload=payload)

@api.put("/project/{id}", auth=auth)
def update(request, payload:ProjectSchema, id: int):
    return project_store(request, payload=payload, id=id)

@api.delete("/project/{id}", auth=auth)
def update(request, id: int):
    return project_delete(request, id=id)