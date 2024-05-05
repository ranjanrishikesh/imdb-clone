from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "password_confirmation": "password"
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="password@123")
        
    def test_login(self):
        data = {
            "username": "testcase",
            "password": "password@123"
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_logout(self):
        self.token = Token.objects.get(user__username='testcase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
