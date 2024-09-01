from ...models import Labels
from ManagementTask.helpers import response_json
from rest_framework import status
from django.utils import timezone
from django.db import IntegrityError, DatabaseError

def label_list(request, id=None):
    if id:
        try:
            label = Labels.objects.get(id=id)
        except Labels.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Label Doesn't Exist")
        
        data = {
            "id": label.id,
            "name": label.name,
            "color": label.color,
            "created_at": label.created_at,
            "updated_at": label.updated_at
        }
    else:
        labels = Labels.objects.all()
        
        data = [
            {
                "id": label.id,
                "name": label.name,
                "color": label.color,
                "created_at": label.created_at,
                "updated_at": label.updated_at
            }
            for label in labels
        ]
        
    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def label_store(request, payload, id=None):
    try:
        if id:
            try:
                label = Labels.objects.get(id=id)
            except Labels.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Label Doesn't Exist")
            
            label.name = payload.name
            label.color = payload.color
            label.updated_at = timezone.now()
            
            label.save()
        else:
            label = Labels.objects.create(
                name=payload.name,
                color=payload.color,
                created_at=timezone.now(),
            )
            
        data = {
            "id": label.id,
            "name": label.name,
            "color": label.color,
        }
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def label_delete(request, id):
    try:
        data = Labels.objects.get(id=id)
    except Labels.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Label Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")