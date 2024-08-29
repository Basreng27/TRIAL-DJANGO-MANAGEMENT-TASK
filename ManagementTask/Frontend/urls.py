from django.urls import path
from .views import *

urlpatterns = [
    path('', page_login, name='login'),
    path('process_login', process_login, name='process-login'),
    path('logout', logout, name='logout'),
    
    path('dashboard', dashboard, name='dashboard'),
]
