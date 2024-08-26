from rest_framework import serializers
from ...models import ProjectMembers

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMembers
        fields = ['id', 'project_id', 'user_id', 'role', 'joined_at', 'resigned_at']