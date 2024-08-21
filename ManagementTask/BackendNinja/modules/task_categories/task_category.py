from ...models import TaskCategories, Categories, Tasks
from ManagementTask.helpers import response_json
from rest_framework import status
from django.db import IntegrityError, DatabaseError

def task_category_list(request, id=None):
    if id:
        try:
            task_category = TaskCategories.objects.get(id=id)
        except TaskCategories.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Task Category Doesn't Exist", None)
        
        data = {
            "id": task_category.id,
            "task_id": task_category.task_id.id,
            "category_id": task_category.category_id.id
        }
    else:
        tasks_categories = TaskCategories.objects.all()
        
        data = [
            {
                "id": task_category.id,
                "task_id": task_category.task_id.id,
                "category_id": task_category.category_id.id
            }
            for task_category in tasks_categories
        ]
        
    return response_json(True, status.HTTP_200_OK, None, data)

def task_category_store(request, payload, id=None):
    try:
        try:
            task = Tasks.objects.get(id=payload.task_id)
        except Tasks.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Task Doesn't Exist", None)
        
        try:
            category = Categories.objects.get(id=payload.category_id)
        except Categories.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Category Doesn't Exist", None)
        
        if id:
            try:
                task_category = TaskCategories.objects.get(id=id)
            except TaskCategories.DoesNotExist:
                return response_json(False, status.HTTP_404_NOT_FOUND, "Task Category Doesn't Exist", None)
            
            task_category.task_id = task
            task_category.category_id = category
            
            task_category.save()
        else:
            task_category = TaskCategories.objects.create(
                task_id=task,
                category_id=category,
            )
            
        data = {
            "id": task_category.id,
            "task_id": task.id,
            "category_id": category.id
        }
        
        return response_json(True, status.HTTP_200_OK, None, data)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)
    
def task_category_delete(request, id):
    try:
        data = TaskCategories.objects.get(id=id)
    except TaskCategories.DoesNotExist:
        return response_json(False, status.HTTP_404_NOT_FOUND, "Task Category Doesn't Exist", None)
    
    try:
        data.delete()
    
        return response_json(True, status.HTTP_200_OK, "Deleted Data", None)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)