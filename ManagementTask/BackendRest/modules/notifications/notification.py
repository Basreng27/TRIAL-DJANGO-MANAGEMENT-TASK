from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ManagementTask.helpers import response_json
from django.shortcuts import get_object_or_404
from ...models import Notifications
from .serializers import NotificationSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError, DatabaseError

class Notification(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        
        if id:
            notification = get_object_or_404(Notifications, id=id)
            status_many = False
        else:
            notification = Notifications.objects.all()
            status_many = True
            
        serializer = NotificationSerializer(notification, many=status_many)
        
        return Response(response_json(status=True, code=status.HTTP_200_OK, data=serializer.data))
    
    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
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
        
        notification = get_object_or_404(Notifications, id=id)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        
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
        notification = get_object_or_404(Notifications, id=id)
        
        try:
            notification.delete()
            
            return Response(response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data"))
        except IntegrityError as ie:
            return Response(response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}"))
        except DatabaseError as de:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}"))
        except Exception as e:
            return Response(response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}"))