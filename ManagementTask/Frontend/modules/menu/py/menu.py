import requests
from django.shortcuts import render
from ...form import MenuForm
from django.urls import reverse
from rest_framework import status
from ManagementTask.helpers import response_frontend
from django.conf import settings
from ...template.py.core import Core

def menu_page(request):
    token = request.COOKIES.get('access_token_api_ninja')

    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="Menu", message='Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'{settings.API_NINJA}menu_parent', headers=headers)

    if response.status_code == 200:
        menus = response.json()

        data = {
            'title': 'Menu',
            'breadcrumbs':{
                'Management',
                'Menu',
            },
            'data': menus['data']
        }
        
        return Core.load_template(request=request, url='menu/pages/display.html', data=data)
    else:
        return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu")

def menu_child(request, id):
    token = request.COOKIES.get('access_token_api_ninja')

    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="Menu", message='Undifined Token')
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'{settings.API_NINJA}menu_parent/{id}', headers=headers)

    if response.status_code == 200:
        menus = response.json()

        data = {
            'data': menus['data'],
            'parent_id': id
        }
        
        return render(request, 'menu/pages/table_child.html', data)
    else:
        return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu")
    
def menu_form(request, id=None):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="Menu", message='Undifined Token')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    if id:
        response = requests.get(f'{settings.API_NINJA}menu/{id}', headers=headers)

        if response.status_code == 200:
            menu = response.json()
            form = MenuForm(request.POST or None, initial=menu['data'])
            url_action = reverse('form-menu-update', kwargs={'id': id})
        else:
            return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu")
    else:
        form = MenuForm(request.POST or None)
        url_action = reverse('form-menu')

    if request.method == 'POST':
        form = MenuForm(request.POST)
        
        if form.is_valid():
            data_input = {
                'parent_id': form.cleaned_data['parent_id'].id if form.cleaned_data['parent_id'] else None,
                'name': form.cleaned_data['name'],
                'url': form.cleaned_data['url'],
                'icon': form.cleaned_data['icon'],
                'sequence': form.cleaned_data['sequence'],
            }
            
            if id:
                response = requests.put(f'{settings.API_NINJA}menu/{id}', json=data_input, headers=headers)
                status_type = 'Updated'
            else:
                response = requests.post(f'{settings.API_NINJA}menu', json=data_input, headers=headers)
                status_type = 'Added'

            if response.status_code in [200, 201]:
                return response_frontend(status=True, code=status.HTTP_200_OK, title="Menu", url='menu', message=f'Successfully {status_type} Data')
            else:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = response.text

                return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu", message=error_data)
        else:
            return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu", message=form.errors.as_json())

    data = {
        'form': form,
        'url_action': url_action,
    }
    
    return render(request, 'menu/pages/form.html', data)

def menu_delete(request, id):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="Menu", message='Undifined Token')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    response = requests.delete(f'{settings.API_NINJA}menu/{id}', headers=headers)

    if response.status_code == 200:
        return response_frontend(status=True, code=status.HTTP_200_OK, title="Menu", url='menu', message='Successfully Deleted Data')
    else:
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu", message=error_data['data'])