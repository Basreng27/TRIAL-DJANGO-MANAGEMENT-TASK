import requests
from django.shortcuts import render
from ...form import UserForm
from django.urls import reverse
from rest_framework import status
from ManagementTask.helpers import response_frontend
from django.conf import settings
from ...template.py.core import Core

def user_page(request):
    token = request.COOKIES.get('access_token_api_ninja')

    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="User", message='Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'{settings.API_NINJA}user', headers=headers)

    if response.status_code == 200:
        users = response.json()

        data = {
            'title': 'User',
            'breadcrumbs':{
                'Management',
                'User',
            },
            'data': users['data']
        }
        
        return Core.load_template(request=request, url='user/pages/display.html', data=data)
    else:
        return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="User")

def user_form(request, id=None):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="User", message='Undifined Token')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    if id:
        response = requests.get(f'{settings.API_NINJA}user/{id}', headers=headers)

        if response.status_code == 200:
            user = response.json()
            form = UserForm(request.POST or None, initial=user['data'])
            url_action = reverse('form-user-update', kwargs={'id': id})
        else:
            return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="User")
    else:
        form = UserForm(request.POST or None)
        url_action = reverse('form-user')

    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            data_input = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            
            if id:
                response = requests.put(f'{settings.API_NINJA}user/{id}', json=data_input, headers=headers)
                status_type = 'Updated'
            else:
                response = requests.post(f'{settings.API_NINJA}user', json=data_input, headers=headers)
                status_type = 'Added'

            if response.status_code in [200, 201]:
                return response_frontend(status=True, code=status.HTTP_200_OK, title="User", url='user', message=f'Successfully {status_type} Data')
            else:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = response.text

                return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="User", message=error_data)
        else:
            return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="User", message=form.errors.as_json())

    data = {
        'form': form,
        'url_action': url_action,
    }
    
    return render(request, 'user/pages/form.html', data)

def user_delete(request, id):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="User", message='Undifined Token')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    response = requests.delete(f'{settings.API_NINJA}user/{id}', headers=headers)

    if response.status_code == 200:
        return response_frontend(status=True, code=status.HTTP_200_OK, title="User", url='user', message='Successfully Deleted Data')
    else:
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="User", message=error_data['data'])