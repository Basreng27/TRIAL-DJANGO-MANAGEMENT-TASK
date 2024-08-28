from django.urls import path
from .views import *

urlpatterns = [
    path('', page_login, name='page-login'),
    path('dashboard', dashboard, name='dashboard'),
]
