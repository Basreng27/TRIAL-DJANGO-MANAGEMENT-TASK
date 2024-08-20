from ...models import Projects
from ManagementTask.helpers import response_json
from rest_framework import status
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError
# from django.shortcuts import get_object_or_404
from django.utils import timezone

def project_list(request, id=None):
    if id :
        # project = get_object_or_404(Projects, id=id)
        
        try:
            project = Projects.objects.get(id=id)
        except Projects.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Project Doesn't Exist", None)
        
        data = {
            "id": project.id,
            "user": project.user_id.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
    else:
        projects = Projects.objects.all()
        
        data = [
            {
                "id": project.id,
                "user": project.user_id.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            }
            for project in projects
        ]
    
    return response_json(True, status.HTTP_200_OK, None, data)

def project_store(request, payload, id=None):
    try:
        try:
            user = User.objects.get(id=payload.user_id)
        except User.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "User Doesn't Exist", None)
        
        if id :
            try:
                project = Projects.objects.get(id=id)
            except Projects.DoesNotExist:
                return response_json(False, status.HTTP_404_NOT_FOUND, "Project Doesn't Exist", None)
            
            project.user_id = user
            project.name = payload.name
            project.description = payload.description
            project.updated_at = timezone.now()
            
            project.save()
        else:
            project = Projects.objects.create(
                user_id=user,
                name=payload.name,
                description=payload.description,
                created_at=timezone.now(),
            )

        data = {
            "user_id": project.user_id.id,
            "name": project.name,
            "description": project.description,
        }
        
        return response_json(True, status.HTTP_200_OK, None, data)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)
    
def project_delete(request, id):
    try:
        data = Projects.objects.get(id=id)
    except Projects.DoesNotExist:
        return response_json(False, status.HTTP_404_NOT_FOUND, "Project Doesn't Exist", None)
    
    try:
        data.delete()
    
        return response_json(True, status.HTTP_200_OK, "Deleted Data", None)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)