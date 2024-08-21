from ...models import TaskLabels, Labels, Tasks
from ManagementTask.helpers import response_json
from rest_framework import status
from django.db import IntegrityError, DatabaseError

def task_label_list(request, id=None):
    if id:
        try:
            task_label = TaskLabels.objects.get(id=id)
        except TaskLabels.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Task Label Doesn't Exist", None)
        
        data = {
            "id": task_label.id,
            "task_id": task_label.task_id.id,
            "label_id": task_label.label_id.id
        }
    else:
        tasks_labels = TaskLabels.objects.all()
        
        data = [
            {
                "id": task_label.id,
                "task_id": task_label.task_id.id,
                "label_id": task_label.label_id.id
            }
            for task_label in tasks_labels
        ]
        
    return response_json(True, status.HTTP_200_OK, None, data)

def task_label_store(request, payload, id=None):
    try:
        try:
            task = Tasks.objects.get(id=payload.task_id)
        except Tasks.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Task Doesn't Exist", None)
        
        try:
            label = Labels.objects.get(id=payload.label_id)
        except Labels.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Label Doesn't Exist", None)
        
        if id:
            try:
                task_label = TaskLabels.objects.get(id=id)
            except TaskLabels.DoesNotExist:
                return response_json(False, status.HTTP_404_NOT_FOUND, "Task Label Doesn't Exist", None)
            
            task_label.task_id = task
            task_label.label_id = label
            
            task_label.save()
        else:
            task_label = TaskLabels.objects.create(
                task_id=task,
                label_id=label,
            )
            
        data = {
            "id": task_label.id,
            "task_id": task.id,
            "label_id": label.id
        }
        
        return response_json(True, status.HTTP_200_OK, None, data)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)
    
def task_label_delete(request, id):
    try:
        data = TaskLabels.objects.get(id=id)
    except TaskLabels.DoesNotExist:
        return response_json(False, status.HTTP_404_NOT_FOUND, "Task Label Doesn't Exist", None)
    
    try:
        data.delete()
    
        return response_json(True, status.HTTP_200_OK, "Deleted Data", None)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)