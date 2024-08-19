import json
import requests
from ManagementTask.helpers import response_json
from rest_framework import status

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
        return response_json(False, status.HTTP_400_BAD_REQUEST, None, None)