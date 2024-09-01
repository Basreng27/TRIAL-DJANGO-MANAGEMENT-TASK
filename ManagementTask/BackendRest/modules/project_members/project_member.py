from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ManagementTask.helpers import response_json
from django.shortcuts import get_object_or_404
from ...models import ProjectMembers
from .serializers import ProjectMemberSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError, DatabaseError

class ProjectMember(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        
        if id:
            project_member = get_object_or_404(ProjectMembers, id=id)
            status_many = False
        else:
            project_member = ProjectMembers.objects.all()
            status_many = True
            
        serializer = ProjectMemberSerializer(project_member, many=status_many)
        
        return Response(response_json(status=True, code=status.HTTP_200_OK, data=serializer.data))
    
    def post(self, request, *args, **kwargs):
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            serializer.save()
            
            return Response(response_json(status=True, code=status.HTTP_201_CREATED, data=serializer.data))
        except IntegrityError as ie:
            return Response(response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}"))
        except DatabaseError as de:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}"))
        except Exception as e:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}"))

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        
        if not id:
            return Response(response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="ID is required for updating"))
        
        project_member = get_object_or_404(ProjectMembers, id=id)
        serializer = ProjectMemberSerializer(project_member, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            
            return Response(response_json(status=True, code=status.HTTP_201_CREATED, data=serializer.data))
        except IntegrityError as ie:
            return Response(response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}"))
        except DatabaseError as de:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}"))
        except Exception as e:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}"))

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        project_member = get_object_or_404(ProjectMembers, id=id)
        
        try:
            project_member.delete()
            
            return Response(response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data"))
        except IntegrityError as ie:
            return Response(response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}"))
        except DatabaseError as de:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}"))
        except Exception as e:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}"))