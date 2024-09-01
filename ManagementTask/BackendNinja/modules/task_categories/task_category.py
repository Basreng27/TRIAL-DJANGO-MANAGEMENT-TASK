from ...models import TaskCategories, Categories, Tasks
from ManagementTask.helpers import response_json
from rest_framework import status
from django.db import IntegrityError, DatabaseError

def task_category_list(request, id=None):
    if id:
        try:
            task_category = TaskCategories.objects.get(id=id)
        except TaskCategories.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Category Doesn't Exist")
        
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
        
    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def task_category_store(request, payload, id=None):
    try:
        try:
            task = Tasks.objects.get(id=payload.task_id)
        except Tasks.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Doesn't Exist")
        
        try:
            category = Categories.objects.get(id=payload.category_id)
        except Categories.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Category Doesn't Exist")
        
        if id:
            try:
                task_category = TaskCategories.objects.get(id=id)
            except TaskCategories.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Category Doesn't Exist")
            
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
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def task_category_delete(request, id):
    try:
        data = TaskCategories.objects.get(id=id)
    except TaskCategories.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Task Category Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")