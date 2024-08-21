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
            return response_json(False, status.HTTP_404_NOT_FOUND, "Label Doesn't Exist", None)
        
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
        
    return response_json(True, status.HTTP_200_OK, None, data)

def label_store(request, payload, id=None):
    try:
        if id:
            try:
                label = Labels.objects.get(id=id)
            except Labels.DoesNotExist:
                return response_json(False, status.HTTP_404_NOT_FOUND, "Label Doesn't Exist", None)
            
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
        
        return response_json(True, status.HTTP_200_OK, None, data)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)
    
def label_delete(request, id):
    try:
        data = Labels.objects.get(id=id)
    except Labels.DoesNotExist:
        return response_json(False, status.HTTP_404_NOT_FOUND, "Label Doesn't Exist", None)
    
    try:
        data.delete()
    
        return response_json(True, status.HTTP_200_OK, "Deleted Data", None)
    except IntegrityError as ie:
        return response_json(False, status.HTTP_400_BAD_REQUEST, f"Integrity Error: {str(ie)}", None)
    except DatabaseError as de:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database Error: {str(de)}", None)
    except Exception as e:
        return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unexpected Error: {str(e)}", None)