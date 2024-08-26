from rest_framework import serializers
from ...models import Notifications

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'user_id', 'content', 'is_read', 'created_at']