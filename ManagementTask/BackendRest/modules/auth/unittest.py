import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class RegisterSerializerTestCase(TestCase):
    def test_valid_registration(self):
        # Declarated Data
        data = {
            'first_name': 'testuser',
            'last_name': 'testuser',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password',
            'confirm_password': 'strong_password'
        }
        
        # Send Data
        serializer = RegisterSerializer(data=data)
        
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        response = serializer.save()
        
        # If Return Object User
        self.assertEqual(response.first_name, 'testuser')
        self.assertEqual(response.last_name, 'testuser')
        self.assertEqual(response.username, 'testuser')
        self.assertEqual(response.email, 'testuser@example.com')
        self.assertTrue(response.check_password('strong_password'))

        # # Decode JSON from JsonResponse
        # response_data = json.loads(response.content)
        # data = response_data['data'][0]
        
        # # Json
        # self.assertEqual(response_data['code'], status.HTTP_201_CREATED)
        # self.assertEqual(data['username'], 'testuser')
        # self.assertEqual(data['email'], 'testuser@example.com')

    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password',
            'confirm_password': 'weak_password'
        }
        
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'non_field_errors'})
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), "Password Do Not Match")

    def test_missing_field(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strong_password',
            # 'confirm_password' field is missing
        }
        
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_password', serializer.errors)

    def test_duplicate_username(self):
        User.objects.create(username='testuser', email='testuser@example.com', password='strong_password')
        
        data = {
            'username': 'testuser',
            'email': 'anotheruser@example.com',
            'password': 'strong_password',
            'confirm_password': 'strong_password'
        }
        
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

class LoginSerializerTestCase(TestCase):
    def setUp(self):
        # Setup user
        self.user = User.objects.create_user(
            username='testuser',
            password='strong_password'
        )

    def test_valid_login(self):
        data = {
            'username': 'testuser',
            'password': 'strong_password'
        }
        
        serializer = LoginSerializer(data=data)
        
        # Test if the serializer is valid
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        # Mock the TokenObtainPairSerializer.validate() method
        response = serializer.validate(data)
        
        # Decode JSON from JsonResponse
        # response_data = json.loads(response.content)
        # data = response_data['data']
        data = response
        
        # Check if response contains tokens
        self.assertIn('refresh', data)
        self.assertIn('access', data)
        
        # Validate tokens
        # refresh = RefreshToken(data['refresh'])
        
        # self.assertEqual(refresh, data['refresh'])
        self.assertEqual(data['username'], 'testuser')

    # def test_invalid_login(self):
    #     # With Wrong Password
    #     data = {
    #         'username': 'superuser',
    #         'password': 'wrong_password'  # Wrong
    #     }
        
    #     serializer = LoginSerializer(data=data)
        
    #     # Test if the serializer is invalid
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('non_field_errors', serializer.errors)

# class LogoutTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.username = 'testuser'
#         self.password = 'strong_password'
#         self.user = User.objects.create_user(username=self.username, password=self.password)
        
#         # Generate tokens for the user
#         self.refresh = RefreshToken.for_user(self.user)
#         self.access_token = str(self.refresh.access_token)
#         self.refresh_token = str(self.refresh)

#     def test_successful_logout(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
#         response = self.client.post('/logout/', {'access': self.access_token})
        
#         response_data = json.loads(response.content)
#         print(f"-------------------------------{response_data}")
#         self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
#         self.assertTrue(response.json()['status'])
#         self.assertEqual(response.json()['message'], "Logged out successfully")

#     def test_missing_token(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
#         response = self.client.post('/logout/', {})
        
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(response.json()['status'])
#         self.assertEqual(response.json()['message'], "Refresh token not provided")

#     def test_invalid_token(self):
#         invalid_token = 'invalid_token'
        
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
#         response = self.client.post('/logout/', {'access': invalid_token})
        
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(response.json()['status'])
#         self.assertEqual(response.json()['message'], "Token is invalid or expired")