"""Product tests."""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.products.models import Product, Category


@pytest.fixture
def category(db):
    """Category fixture."""
    return Category.objects.create(
        name='Electronics',
        description='Electronic products'
    )


@pytest.fixture
def product(db, category):
    """Product fixture."""
    return Product.objects.create(
        name='Laptop',
        slug='laptop',
        description='High performance laptop',
        price='999.99',
        stock=10,
        category=category
    )


@pytest.mark.django_db
class TestProductList:
    """Test product listing."""
    
    def test_list_products(self, api_client, product):
        """Test listing products."""
        url = reverse('product-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_search_products(self, api_client, product):
        """Test product search."""
        url = reverse('product-list')
        response = api_client.get(url, {'search': 'Laptop'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0


@pytest.mark.django_db
class TestProductCreate:
    """Test product creation."""
    
    def test_create_product_unauthorized(self, api_client, category):
        """Test creating product without authentication."""
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'Test product',
            'price': '99.99',
            'stock': 5,
            'category': category.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_product_as_admin(self, admin_client, category):
        """Test creating product as admin."""
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'Test product',
            'price': '99.99',
            'stock': 5,
            'category': category.id
        }
        response = admin_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name='New Product').exists()
