from ...models import Tasks, Projects
from ManagementTask.helpers import response_json
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError, DatabaseError

def task_list(request, id=None):
    if id:
        try:
            task = Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Doesn't Exist")
        
        data = {
            "id": task.id,
            "project_id": task.project_id.id,
            "assigned_user_id": task.assigned_user_id.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
    else:
        tasks = Tasks.objects.all()
        
        data = [
            {
                "id": task.id,
                "assigned_user_id": task.assigned_user_id.id,
                "project_id": task.project_id.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            for task in tasks
        ]
        
    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def task_store(request, payload, id=None):
    try:
        try:
            user = User.objects.get(id=payload.assigned_user_id)
        except User.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="User Doesn't Exist")
        
        try:
            project = Projects.objects.get(id=payload.project_id)
        except Projects.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Project Doesn't Exist")
        
        if id:
            try:
                task = Tasks.objects.get(id=id)
            except Tasks.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Doesn't Exist")
            
            task.assigned_user_id = user
            task.project_id = project
            task.title = payload.title
            task.description = payload.description
            task.status = payload.status
            task.priority = payload.priority
            task.due_date = payload.due_date
            task.updated_at = timezone.now()
            
            task.save()
        else:
            task = Tasks.objects.create(
                assigned_user_id=user,
                project_id=project,
                title=payload.title,
                description=payload.description,
                status=payload.status,
                priority=payload.priority,
                due_date=payload.due_date,
                created_at=timezone.now(),
            )
            
        data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id.id,
            "assigned_user_id": task.assigned_user_id.id,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
        }
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def task_delete(request, id):
    try:
        data = Tasks.objects.get(id=id)
    except Tasks.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")