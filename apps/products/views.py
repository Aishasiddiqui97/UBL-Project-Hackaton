"""Product views."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from apps.users.permissions import IsManager


@extend_schema_view(
    list=extend_schema(description='List all categories'),
    retrieve=extend_schema(description='Get category details'),
    create=extend_schema(description='Create category (Manager/Admin only)'),
    update=extend_schema(description='Update category (Manager/Admin only)'),
    destroy=extend_schema(description='Delete category (Manager/Admin only)'),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """Category CRUD operations."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManager()]
        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(description='List all products'),
    retrieve=extend_schema(description='Get product details'),
    create=extend_schema(description='Create product (Manager/Admin only)'),
    update=extend_schema(description='Update product (Manager/Admin only)'),
    destroy=extend_schema(description='Delete product (Manager/Admin only)'),
)
class ProductViewSet(viewsets.ModelViewSet):
    """Product CRUD operations."""
    queryset = Product.objects.select_related('category').filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManager()]
        return super().get_permissions()
