from ...models import Categories
from ManagementTask.helpers import response_json
from rest_framework import status
from django.utils import timezone
from django.db import IntegrityError, DatabaseError

def category_list(request, id=None):
    if id:
        try:
            category = Categories.objects.get(id=id)
        except Categories.DoesNotExist:
            return response_json(False, status.HTTP_404_NOT_FOUND, "Category Doesn't Exist", None)
        
        data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
    else:
        categories = Categories.objects.all()
        
        data = [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
            }
            for category in categories
        ]

    return response_json(True, status.HTTP_200_OK, None, data)

def category_store(request, payload, id=None):
    try:
        if id:
            try:
                category = Categories.objects.get(id=id)
            except Categories.DoesNotExist:
                return response_json(False, status.HTTP_404_NOT_FOUND, "Category Doesn't Exist", None)
            
            category.name = payload.name
            category.description = payload.description
            category.updated_at = timezone.now()
        
            category.save()
        else:
            category = Categories.objects.create(
                name=payload.name,
                description=payload.description,
                created_at=timezone.now(),
            )

        data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
        }
        
        return response_json(True, status.HTTP_200_OK, None, data)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)
    
def category_delete(request, id):
    try:
        data = Categories.objects.get(id=id)
    except Categories.DoesNotExist:
        return response_json(False, status.HTTP_404_NOT_FOUND, "Category Doesn't Exist", None)
    
    try:
        data.delete()
    
        return response_json(True, status.HTTP_200_OK, "Deleted Data", None)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)