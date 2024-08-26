from rest_framework import serializers
from ...models import FileAttachments

class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachments
        fields = ['id', 'task_id', 'project_id', 'file', 'uploaded_at']