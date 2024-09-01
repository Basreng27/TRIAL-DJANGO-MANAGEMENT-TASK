from django.urls import path
from .views import *

urlpatterns = [
    path('', page_login, name='page-login'),
    path('process_login', process_login, name='process-login'),
    path('logout', logout, name='logout'),
    
    path('dashboard', dashboard, name='dashboard'),
    
    path('menu', menu, name='menu'),
    path('menu-form', form_menu, name='form-menu'),
    path('menu-form/<int:id>', form_menu, name='form-menu-update'),
    path('menu-delete/<int:id>', delete_menu, name='delete-menu'),
]