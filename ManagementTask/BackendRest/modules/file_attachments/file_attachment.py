from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ManagementTask.helpers import response_json
from django.shortcuts import get_object_or_404
from ...models import FileAttachments
from .serializers import FileAttachmentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError, DatabaseError

class FileAttachment(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        
        if id:
            file_attachment = get_object_or_404(FileAttachments, id=id)
            status_many = False
        else:
            file_attachment = FileAttachments.objects.all()
            status_many = True
            
        serializer = FileAttachmentSerializer(file_attachment, many=status_many)
        
        return Response(response_json(True, status.HTTP_200_OK, None, serializer.data))
    
    def post(self, request, *args, **kwargs):
        serializer = FileAttachmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            serializer.save()
            
            return Response(response_json(True, status.HTTP_201_CREATED, None, serializer.data))
        except IntegrityError as ie:
            return Response(response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None))
        except DatabaseError as de:
            return Response(response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None))
        except Exception as e:
            return Response(response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None))

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        
        if not id:
            return Response(response_json(False, status.HTTP_400_BAD_REQUEST, "ID is required for updating", None))
        
        file_attachment = get_object_or_404(FileAttachments, id=id)
        serializer = FileAttachmentSerializer(file_attachment, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            
            return Response(response_json(True, status.HTTP_201_CREATED, None, serializer.data))
        except IntegrityError as ie:
            return Response(response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None))
        except DatabaseError as de:
            return Response(response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None))
        except Exception as e:
            return Response(response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None))

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        file_attachment = get_object_or_404(FileAttachments, id=id)
        
        try:
            file_attachment.delete()
            
            return Response(response_json(True, status.HTTP_200_OK, "Deleted Data", None))
        except IntegrityError as ie:
            return Response(response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None))
        except DatabaseError as de:
            return Response(response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None))
        except Exception as e:
            return Response(response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None))