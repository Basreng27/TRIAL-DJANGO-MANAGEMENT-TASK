from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ManagementTask.helpers import response_json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class Login(TokenObtainPairView):
    serializer_class = LoginSerializer

class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Ambil token refresh dari header Authorization
            token = request.data.get('access')
            if token is None:
                return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="Refresh token not provided")
            
            # Tambahkan token ke blacklist
            RefreshToken(token).blacklist()

            return response_json(status=True, code=status.HTTP_205_RESET_CONTENT, message="Logged out successfully")
        except TokenError:
            return response_json(status=False, code=status.HTTP_400_BAD_REQUEST, message="Token is invalid or expired")
