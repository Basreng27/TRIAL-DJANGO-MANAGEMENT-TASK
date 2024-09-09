import requests
from django.shortcuts import render
from ManagementTask.helpers import response_frontend, get_url_name
from rest_framework import status
from django.conf import settings

class Core:    
    def load_template(request, url, data:None):
        data['menu'] = request.session.get('menu', [])
        data['url_name'] = get_url_name(request.build_absolute_uri())
        
        return render(request, url, data)
        
        
    def set_session_menu(request):
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
            
            request.session['menu'] = tamp
        else:
            return response_frontend(status=False, code=status.HTTP_404_NOT_FOUND, title="Menu")