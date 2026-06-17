"""Pytest configuration."""
import pytest
from rest_framework.test import APIClient
from apps.users.models import User, UserRole


@pytest.fixture
def api_client():
    """API client fixture."""
    return APIClient()


@pytest.fixture
def user(db):
    """Regular user fixture."""
    return User.objects.create_user(
        email='user@example.com',
        username='user',
        full_name='Regular User',
        password='TestPassword123!'
    )


@pytest.fixture
def admin_user(db):
    """Admin user fixture."""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        full_name='Admin User',
        password='AdminPassword123!'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated API client fixture."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Admin authenticated API client fixture."""
    api_client.force_authenticate(user=admin_user)
    return api_client
