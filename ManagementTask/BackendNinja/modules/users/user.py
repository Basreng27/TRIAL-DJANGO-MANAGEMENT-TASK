from django.contrib.auth.models import User
from ManagementTask.helpers import response_json
from rest_framework import status
from django.db import IntegrityError, DatabaseError

def user_list(request, id=None):
    if id:
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="User Doesn't Exist")

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    else:
        users = User.objects.all()
        
        data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            for user in users
        ]

    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def user_store(request, payload, id=None):
    try:
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="User Doesn't Exist")
            
            user.username = payload.username
            user.password = payload.password
            user.email = payload.email
            user.first_name = payload.first_name
            user.last_name = payload.last_name
            
            if payload.password:
                user.set_password(payload.password)

            user.save()
        else:
            user = User.objects.create(
                username=payload.username,
                password=payload.password,
                email=payload.email,
                first_name=payload.first_name,
                last_name=payload.last_name,
            )
            
            user.set_password(payload.password)
            user.save()
            
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def user_delete(request, id):
    try:
        data = User.objects.get(id=id)
    except User.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="User Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")