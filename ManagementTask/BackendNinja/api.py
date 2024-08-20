from ninja import NinjaAPI
from ninja.security import HttpBearer
from .models import BlacklistedToken
from ManagementTask.helpers import response_json
from rest_framework import status
from jwt import decode as jwt_decode, exceptions, ExpiredSignatureError
from django.conf import settings
from django.contrib.auth.models import User
from .modules.auth.schema import LoginSchema
from .modules.auth.auth import login_process, logout_process
from .modules.projects.schema import ProjectSchema
from .modules.projects.project import project_list, project_store, project_delete
from .modules.tasks.schema import TaskSchema
from .modules.tasks.task import task_list, task_store, task_delete

api = NinjaAPI()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if BlacklistedToken.objects.filter(token=token).exists():
            return None
        
        try:
            decode = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            return User.objects.get(id=decode['user_id'])
        except ExpiredSignatureError:
            return None
        except (exceptions.DecodeError, User.DoesNotExist):
            return None

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

# Task
@api.get("/task", auth=auth)
def get_list(request):
    return task_list(request)

@api.get("/task/{id}", auth=auth)
def get(request, id: int):
    return task_list(request, id=id)

@api.post("/task", auth=auth)
def create(request, payload:TaskSchema):
    return task_store(request, payload=payload)

@api.put("/task/{id}", auth=auth)
def update(request, payload:TaskSchema, id: int):
    return task_store(request, payload=payload, id=id)

@api.delete("/task/{id}", auth=auth)
def update(request, id: int):
    return task_delete(request, id=id)