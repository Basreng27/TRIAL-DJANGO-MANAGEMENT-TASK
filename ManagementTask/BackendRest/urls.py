from django.urls import path
from .modules.auth.auth import Login, Register, Logout
from .modules.project_members.project_member import ProjectMember

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    
    path('project_member', ProjectMember.as_view(), name='project-member'),
    path('project_member/<int:id>', ProjectMember.as_view(), name='project-member-detail')
]