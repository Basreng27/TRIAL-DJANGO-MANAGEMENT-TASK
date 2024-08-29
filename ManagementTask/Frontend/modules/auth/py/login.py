import json
import requests
from ManagementTask.helpers import response_json
from rest_framework import status
from ...form import LoginForm
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

base_url = 'http://localhost:8000/'

def get_token_ninja(username, password):
    url = f'{base_url}api-ninja/login'
    data = {
        "username":username,
        "password":password
    }
    
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        return response.json()
    else:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST)

def get_token_rest(username, password):
    url = f'{base_url}api-rest/login'
    data = {
        "username": username,
        "password": password,
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST)

def get_token(user):
    refresh = RefreshToken.for_user(user)

    if refresh:
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    else:
        return response_json(status=False, code=status.HTTP_400_BAD_REQUEST)

def login_data(request=None):
    return {
        'title': 'Login',
        'form': LoginForm(request.POST or None),
        'url_action': reverse('process-login'),
    }

def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                token_rest = get_token_rest(username, password)
                token_ninja = get_token_ninja(username, password)

                tokens = get_token(user)
                
                response = HttpResponse(response_json(status=True, code=status.HTTP_200_OK, message="Successfully Login"))

                response.set_cookie('access_token', tokens['access'], httponly=True)
                response.set_cookie('access_token_api_rest', token_rest['data']['access_rest'], httponly=True)
                response.set_cookie('access_token_api_ninja', token_ninja['data']['token'], httponly=True)

                # return response
                return redirect('dashboard')
            else:
                return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="Wrong Username Or Password")
        else:
            return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="Empty Username Or Password")

    return redirect('login')