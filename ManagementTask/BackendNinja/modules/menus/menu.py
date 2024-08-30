from ...models import Menus
from ManagementTask.helpers import response_json
from rest_framework import status
from django.db import IntegrityError, DatabaseError

def menu_list(request, id=None):
    if id:
        try:
            menu = Menus.objects.get(id=id)
        except Menus.DoesNotExist:
            return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Menu Doesn't Exist")

        data = {
            "id": menu.id,
            "parent_id": menu.parent_id.id if menu.parent_id else menu.parent_id,
            "name": menu.name,
            "url": menu.url,
            "icon": menu.icon,
            "sequence": menu.sequence,
        }
    else:
        menus = Menus.objects.all()
        
        data = [
            {
                "id": menu.id,
                "parent_id": menu.parent_id.id if menu.parent_id else menu.parent_id,
                "name": menu.name,
                "url": menu.url,
                "icon": menu.icon,
                "sequence": menu.sequence,
            }
            for menu in menus
        ]

    return response_json(status=True, code=status.HTTP_200_OK, data=data)

def menu_store(request, payload, id=None):
    try:
        parent_menu = None

        if payload.parent_id:
            try:
                parent_menu = Menus.objects.get(id=payload.parent_id)
            except Menus.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Menu Doesn't Exist")

        if id:
            try:
                menu = Menus.objects.get(id=id)
            except Menus.DoesNotExist:
                return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Menu Doesn't Exist")
            
            menu.parent_id = parent_menu
            menu.name = payload.name
            menu.url = payload.url
            menu.icon = payload.icon
            menu.sequence = payload.sequence
            
            menu.save()
        else:
            menu = Menus.objects.create(
                parent_id = parent_menu,
                name=payload.name,
                url=payload.url,
                icon=payload.icon,
                sequence=payload.sequence,
            )
            
        data = {
            "id": menu.id,
            "parent_id": menu.parent_id.id if menu.parent_id else menu.parent_id,
            "name": menu.name,
            "url": menu.url,
            "icon": menu.icon,
            "sequence": menu.sequence,
        }
        
        return response_json(status=True, code=status.HTTP_200_OK, data=data)
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")
    
def menu_delete(request, id):
    try:
        data = Menus.objects.get(id=id)
    except Menus.DoesNotExist:
        return response_json(status=False, code=status.HTTP_404_NOT_FOUND, message="Menu Doesn't Exist")
    
    try:
        data.delete()
    
        return response_json(status=True, code=status.HTTP_200_OK, message="Deleted Data")
    except IntegrityError as ie:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message=f"Integrity Error: {str(ie)}")
    except DatabaseError as de:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Database Error: {str(de)}")
    except Exception as e:
        return response_json(status=False, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Unexpected Error: {str(e)}")