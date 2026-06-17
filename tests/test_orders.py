"""Order tests."""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.orders.models import Order
from apps.products.models import Product, Category


@pytest.fixture
def category(db):
    """Category fixture."""
    return Category.objects.create(name='Test Category')


@pytest.fixture
def product(db, category):
    """Product fixture."""
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        description='Test description',
        price='50.00',
        stock=10,
        category=category
    )


@pytest.mark.django_db
class TestOrderCreation:
    """Test order creation."""
    
    def test_create_order(self, authenticated_client, product):
        """Test creating an order."""
        url = reverse('order-list')
        data = {
            'shipping_address': '123 Test St',
            'notes': 'Test order',
            'items': [
                {
                    'product': product.id,
                    'quantity': 2
                }
            ]
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
    
    def test_create_order_insufficient_stock(self, authenticated_client, product):
        """Test order with insufficient stock."""
        url = reverse('order-list')
        data = {
            'shipping_address': '123 Test St',
            'items': [
                {
                    'product': product.id,
                    'quantity': 100  # More than available stock
                }
            ]
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
