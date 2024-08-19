import logging
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ManagementTask.helpers import response_json
from rest_framework import status, serializers
from django.contrib.auth.models import User
from django.db import DatabaseError

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh_rest = self.get_token(self.user)
        
        data = {
            'username': self.user.username,
            'refresh_rest': str(refresh_rest),
            'access_rest': str(refresh_rest.access_token)
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
            
            logger.info(f"=== User created: {user.username}")

            return response_json(True, status.HTTP_201_CREATED, None, user)
        except DatabaseError as db_error:
            logger.error(f"=== Database error: {db_error}")
            
            return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, str(db_error), None)
        except Exception as e:
            logger.error(f"=== Exception occurred: {e}")
            
            return response_json(False, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), None)