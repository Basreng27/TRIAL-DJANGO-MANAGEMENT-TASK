from django.db import models
from BackendNinja.models import Projects, Tasks
from django.contrib.auth.models import User
from ManagementTask.constant import ListConstant
from django.utils import timezone

# Table ProjectMembers: (Done)
class ProjectMembers(models.Model):
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ListConstant.ROLE_CHOISES, default='MEMBER')
    joined_at = models.DateTimeField(default=timezone.now)
    resigned_at = models.DateTimeField(null=True)

# Table Notifications: (Done)
class Notifications(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

# Table ActivityLogs: (Done)
class ActivityLogs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ListConstant.ACTION_ACTIVITY_LOG_CHOISES, default='CREATED')

# Table FileAttachments:
class FileAttachments(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='ManagementTask/public/files/', blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)