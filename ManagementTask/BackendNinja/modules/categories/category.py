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
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Category Doesn't Exist")
        
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

    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def category_store(request, payload, id=None):
    try:
        if id:
            try:
                category = Categories.objects.get(id=id)
            except Categories.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Category Doesn't Exist")
            
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
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def category_delete(request, id):
    try:
        data = Categories.objects.get(id=id)
    except Categories.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Category Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")