from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ManagementTask.helpers import response_json
from django.shortcuts import get_object_or_404
from ...models import ActivityLogs
from .serializers import ActivityLogSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError, DatabaseError

class ActivityLog(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        
        if id:
            activity_log = get_object_or_404(ActivityLogs, id=id)
            status_many = False
        else:
            activity_log = ActivityLogs.objects.all()
            status_many = True
            
        serializer = ActivityLogSerializer(activity_log, many=status_many)
        
        return Response(response_json(status=True, code=status.HTTP_200_OK, data=serializer.data))
    
    def post(self, request, *args, **kwargs):
        serializer = ActivityLogSerializer(data=request.data)
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
        
        activity_log = get_object_or_404(ActivityLogs, id=id)
        serializer = ActivityLogSerializer(activity_log, data=request.data, partial=True)
        
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
        activity_log = get_object_or_404(ActivityLogs, id=id)
        
        try:
            activity_log.delete()
            
            return Response(response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data"))
        except IntegrityError as ie:
            return Response(response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}"))
        except DatabaseError as de:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}"))
        except Exception as e:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}"))