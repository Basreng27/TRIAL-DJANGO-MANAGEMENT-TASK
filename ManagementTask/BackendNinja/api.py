from ninja import NinjaAPI
from ninja.security import HttpBearer
from .models import BlacklistedToken
from jwt import decode as jwt_decode, exceptions, ExpiredSignatureError
from django.conf import settings
from django.contrib.auth.models import User
from .modules.auth.schema import LoginSchema
from .modules.auth.auth import login_process, logout_process
from .modules.projects.schema import ProjectSchema
from .modules.projects.project import project_list, project_store, project_delete
from .modules.tasks.schema import TaskSchema
from .modules.tasks.task import task_list, task_store, task_delete
from .modules.categories.schema import CategorySchema
from .modules.categories.category import category_list, category_store, category_delete
from .modules.task_categories.schema import TaskCategorySchema
from .modules.task_categories.task_category import task_category_list, task_category_store, task_category_delete
from .modules.labels.schema import LabelSchema
from .modules.labels.label import label_list, label_store, label_delete
from .modules.task_labels.schema import TaskLabelSchema
from .modules.task_labels.task_label import task_label_list, task_label_store, task_label_delete
from .modules.menus.schema import MenuSchema
from .modules.menus.menu import menu_list, menu_store, menu_delete, menu_parent_list
from .modules.users.schema import UserSchema
from .modules.users.user import user_list, user_store, user_delete

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

# Category
@api.get("/category", auth=auth)
def get_list(request):
    return category_list(request)

@api.get("/category/{id}", auth=auth)
def get(request, id: int):
    return category_list(request, id=id)

@api.post("/category", auth=auth)
def create(request, payload:CategorySchema):
    return category_store(request, payload=payload)

@api.put("/category/{id}", auth=auth)
def update(request, payload:CategorySchema, id: int):
    return category_store(request, payload=payload, id=id)

@api.delete("/category/{id}", auth=auth)
def update(request, id: int):
    return category_delete(request, id=id)

# Task Category
@api.get("/task_category", auth=auth)
def get_list(request):
    return task_category_list(request)

@api.get("/task_category/{id}", auth=auth)
def get(request, id: int):
    return task_category_list(request, id=id)

@api.post("/task_category", auth=auth)
def create(request, payload:TaskCategorySchema):
    return task_category_store(request, payload=payload)

@api.put("/task_category/{id}", auth=auth)
def update(request, payload:TaskCategorySchema, id: int):
    return task_category_store(request, payload=payload, id=id)

@api.delete("/task_category/{id}", auth=auth)
def update(request, id: int):
    return task_category_delete(request, id=id)

# Label
@api.get("/label", auth=auth)
def get_list(request):
    return label_list(request)

@api.get("/label/{id}", auth=auth)
def get(request, id: int):
    return label_list(request, id=id)

@api.post("/label", auth=auth)
def create(request, payload:LabelSchema):
    return label_store(request, payload=payload)

@api.put("/label/{id}", auth=auth)
def update(request, payload:LabelSchema, id: int):
    return label_store(request, payload=payload, id=id)

@api.delete("/label/{id}", auth=auth)
def update(request, id: int):
    return label_delete(request, id=id)

# Task Category
@api.get("/task_label", auth=auth)
def get_list(request):
    return task_label_list(request)

@api.get("/task_label/{id}", auth=auth)
def get(request, id: int):
    return task_label_list(request, id=id)

@api.post("/task_label", auth=auth)
def create(request, payload:TaskLabelSchema):
    return task_label_store(request, payload=payload)

@api.put("/task_label/{id}", auth=auth)
def update(request, payload:TaskLabelSchema, id: int):
    return task_label_store(request, payload=payload, id=id)

@api.delete("/task_label/{id}", auth=auth)
def update(request, id: int):
    return task_label_delete(request, id=id)

# Menu Category
@api.get("/menu", auth=auth)
def get_list(request):
    return menu_list(request)

@api.get("/menu/{id}", auth=auth)
def get(request, id: int):
    return menu_list(request, id=id)

@api.get("/menu_parent", auth=auth)
def get_parent_list(request):
    return menu_parent_list(request)

@api.get("/menu_parent/{id}", auth=auth)
def get_parent_list(request, id: int):
    return menu_parent_list(request, id=id)

@api.post("/menu", auth=auth)
def create(request, payload:MenuSchema):
    return menu_store(request, payload=payload)

@api.put("/menu/{id}", auth=auth)
def update(request, payload:MenuSchema, id: int):
    return menu_store(request, payload=payload, id=id)

@api.delete("/menu/{id}", auth=auth)
def update(request, id: int):
    return menu_delete(request, id=id)

# User Category
@api.get("/user", auth=auth)
def get_list(request):
    return user_list(request)

@api.get("/user/{id}", auth=auth)
def get(request, id: int):
    return user_list(request, id=id)

@api.post("/user", auth=auth)
def create(request, payload:UserSchema):
    return user_store(request, payload=payload)

@api.put("/user/{id}", auth=auth)
def update(request, payload:UserSchema, id: int):
    return user_store(request, payload=payload, id=id)

@api.delete("/user/{id}", auth=auth)
def update(request, id: int):
    return user_delete(request, id=id)