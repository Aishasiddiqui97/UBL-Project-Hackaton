"""Authentication tests."""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def api_client():
    """API client fixture."""
    return APIClient()


@pytest.fixture
def user_data():
    """User test data fixture."""
    return {
        'email': 'test@example.com',
        'username': 'testuser',
        'full_name': 'Test User',
        'password': 'TestPassword123!',
        'password_confirm': 'TestPassword123!'
    }


@pytest.mark.django_db
class TestRegistration:
    """Test user registration."""
    
    def test_register_success(self, api_client, user_data):
        """Test successful user registration."""
        url = reverse('register')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert User.objects.filter(email=user_data['email']).exists()
    
    def test_register_duplicate_email(self, api_client, user_data):
        """Test registration with duplicate email."""
        User.objects.create_user(**user_data)
        url = reverse('register')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False


@pytest.mark.django_db
class TestLogin:
    """Test user login."""
    
    def test_login_success(self, api_client, user_data):
        """Test successful login."""
        User.objects.create_user(**user_data)
        url = reverse('login')
        response = api_client.post(url, {
            'email': user_data['email'],
            'password': user_data['password']
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access_token' in response.data['data']
        assert 'refresh_token' in response.data['data']
    
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        url = reverse('login')
        response = api_client.post(url, {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False
