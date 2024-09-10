from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('', page_login, name='page-login'),
    path('process_login', process_login, name='process-login'),
    path('logout', logout, name='logout'),
    
    # Dashboard
    path('dashboard', dashboard, name='dashboard'),
    
    # Menu
    path('menu', menu, name='menu'),
    path('menu-form', form_menu, name='form-menu'),
    path('menu-child/<int:id>', child_menu, name='child-menu'),
    path('menu-form/<int:id>', form_menu, name='form-menu-update'),
    path('menu-delete/<int:id>', delete_menu, name='delete-menu'),
    
    # User
    path('user', user, name='user'),
    path('user-form', form_user, name='form-user'),
    path('user-form/<int:id>', form_user, name='form-user-update'),
    path('user-delete/<int:id>', delete_user, name='delete-user'),
]