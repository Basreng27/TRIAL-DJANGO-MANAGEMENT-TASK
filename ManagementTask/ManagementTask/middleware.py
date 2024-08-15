from .helpers import response_json
from rest_framework import status

class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if response.status_code == 404:
            return response_json(False, status.HTTP_400_BAD_REQUEST, "Path doesn't exist")

        return response