from django.urls import path
from .modules.auth.auth import Login, Register, Logout
from .modules.project_members.project_member import ProjectMember
from .modules.notifications.notification import Notification

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    
    path('project_member', ProjectMember.as_view(), name='project-member'),
    path('project_member/<int:id>', ProjectMember.as_view(), name='project-member-detail'),
    
    path('notification', Notification.as_view(), name='notification'),
    path('notification/<int:id>', Notification.as_view(), name='notification-detail')
]