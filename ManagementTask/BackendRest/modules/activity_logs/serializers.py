from rest_framework import serializers
from ...models import ActivityLogs

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLogs
        fields = ['id', 'user_id', 'task_id', 'project_id', 'action']