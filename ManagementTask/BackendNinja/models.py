from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ManagementTask.constant import ListConstant

# Table Projects:
class Projects(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

# Table Tasks:
class Tasks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ListConstant.STATUS_TASK_CHOISES, default='PENDING')
    priority = models.CharField(max_length=10, choices=ListConstant.STATUS_PRIORITY_CHOISES, default='LOW')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

# Table Categories:
class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

# Table TaskCategories:
class TaskCategories(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)

# Table Labels:
class Labels(models.Model):
    name = models.TextField()
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    
# Table TaskLabels:
class TaskLabels(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label_id = models.ForeignKey(Labels, on_delete=models.CASCADE)
    
class BlacklistedToken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    