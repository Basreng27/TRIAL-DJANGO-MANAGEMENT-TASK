from .helpers import response_json
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

User = get_user_model()

class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if response.status_code == 404:
            return response_json(False, status.HTTP_400_BAD_REQUEST, "Path doesn't exist")

        return response

class JWTAuthMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.path.startswith('/api-rest/') or request.path.startswith('/api-ninja/'):
            token = request.COOKIES.get('access_token') or request.headers.get('Authorization')
            
            paths = [
                reverse('login')
            ]

            if token:
                if token.startswith('Bearer '):
                    token = token.split(' ')[1]
                    
                if request.path.startswith('/api-rest/'):
                    try:
                        access = AccessToken(token)
                        user_id = access['user_id']
                        request.user = User.objects.get(id=user_id)
                    except:
                        return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if request.path not in paths:
                    return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            token = request.COOKIES.get('access_token')
            
            paths = [
                reverse('login'),
                reverse('process-login')
            ]
            
            if token:
                try:
                    access = AccessToken(token)
                    user_id = access['user_id']
                    request.user = User.objects.get(id=user_id)
                except Exception:
                    response = HttpResponseRedirect('/management-task/')
                    response.delete_cookie('access_token')
                    
                    return response
            else:
                if request.path not in paths:
                    return redirect('login')
        
        if not hasattr(request, 'user'):
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()

        return self.get_response(request)