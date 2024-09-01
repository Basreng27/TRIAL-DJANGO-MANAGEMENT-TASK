from ...models import TaskLabels, Labels, Tasks
from ManagementTask.helpers import response_json
from rest_framework import status
from django.db import IntegrityError, DatabaseError

def task_label_list(request, id=None):
    if id:
        try:
            task_label = TaskLabels.objects.get(id=id)
        except TaskLabels.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Label Doesn't Exist")
        
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
        
    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def task_label_store(request, payload, id=None):
    try:
        try:
            task = Tasks.objects.get(id=payload.task_id)
        except Tasks.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Doesn't Exist")
        
        try:
            label = Labels.objects.get(id=payload.label_id)
        except Labels.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Label Doesn't Exist")
        
        if id:
            try:
                task_label = TaskLabels.objects.get(id=id)
            except TaskLabels.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Label Doesn't Exist")
            
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
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def task_label_delete(request, id):
    try:
        data = TaskLabels.objects.get(id=id)
    except TaskLabels.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Label Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")