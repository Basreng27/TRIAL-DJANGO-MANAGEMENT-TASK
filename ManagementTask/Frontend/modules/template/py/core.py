import requests
from django.shortcuts import render
from ManagementTask.helpers import response_frontend
from rest_framework import status
from django.conf import settings

class Core:    
    def load_template(request, url, data:None):
        token = request.COOKIES.get('access_token_api_ninja')
        
        if not token:
            return response_frontend(status=False, code=status.HTTP_401_UNAUTHORIZED, title="Menu", message='Undifined Token')
        
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(f'{settings.API_NINJA}menu_parent', headers=headers)

        if response.status_code == 200:
            menus = response.json()

            tamp =[]
            for m in menus['data']:
                response_child = requests.get(f'{settings.API_NINJA}menu_parent/{m["id"]}', headers=headers)
                
                if response_child.status_code == 200:
                    m['child'] = response_child.json().get('data', [])
                
                tamp.append(m)
            
            data['menu'] = tamp 
            
            return render(request, url, data)
        else:
            return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu")
        