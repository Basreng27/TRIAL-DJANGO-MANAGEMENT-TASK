from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ManagementTask.helpers import response_json
from rest_framework import status, serializers
from django.contrib.auth.models import User
from django.db import DatabaseError
from Frontend.modules.auth.py.login import get_token_ninja
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        
        data = super().validate(attrs)
        
        refresh_rest = self.get_token(self.user)
        ninja_token = get_token_ninja(attrs['username'], attrs['password'])

        data = {
            'username': self.user.username,
            'refresh_rest': str(refresh_rest),
            'access_rest': str(refresh_rest.access_token),
            'access_ninja': str(ninja_token['data']['token']),
        }
        
        return response_json(True, status.HTTP_200_OK, None, data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')
        
    def validate(self, payload):
        if payload['password'] != payload['confirm_password']:
            raise serializers.ValidationError("Password Do Not Match")
        
        return payload
    
    def create(self, validated_data):
        # Remove Confirm Password
        validated_data.pop('confirm_password')

        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])
        
        try:
            user.save()

            # return response_json(True, status.HTTP_201_CREATED, None, user)
            return user
        except DatabaseError as db_error:
            return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, str(db_error), None)
        except Exception as e:
            return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), None)
