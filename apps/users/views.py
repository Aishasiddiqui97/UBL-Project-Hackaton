"""User views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin


@extend_schema_view(
    list=extend_schema(description='List all users (Admin only)'),
    retrieve=extend_schema(description='Get user details'),
    create=extend_schema(description='Create new user (Admin only)'),
    update=extend_schema(description='Update user'),
    partial_update=extend_schema(description='Partially update user'),
    destroy=extend_schema(description='Delete user (Admin only)'),
)
class UserViewSet(viewsets.ModelViewSet):
    """User CRUD operations."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'full_name']
    ordering_fields = ['created_at', 'email']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            return [IsAdmin()]
        if self.action in ['update', 'partial_update']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response({
            'success': True,
            'message': 'User profile retrieved',
            'data': serializer.data
        })
