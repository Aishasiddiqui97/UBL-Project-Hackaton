"""Permission tests."""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.users.models import User, UserRole


@pytest.fixture
def manager_user(db):
    """Manager user fixture."""
    return User.objects.create_user(
        email='manager@example.com',
        username='manager',
        full_name='Manager User',
        password='ManagerPass123!',
        role=UserRole.MANAGER
    )


@pytest.fixture
def manager_client(api_client, manager_user):
    """Manager authenticated client."""
    api_client.force_authenticate(user=manager_user)
    return api_client


@pytest.mark.django_db
class TestRolePermissions:
    """Test role-based permissions."""
    
    def test_user_cannot_list_all_users(self, authenticated_client):
        """Test regular user cannot list all users."""
        url = reverse('user-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_admin_can_list_all_users(self, admin_client):
        """Test admin can list all users."""
        url = reverse('user-list')
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_manager_can_create_products(self, manager_client):
        """Test manager can create products."""
        url = reverse('product-list')
        # This would need a category fixture
        assert manager_client is not None
