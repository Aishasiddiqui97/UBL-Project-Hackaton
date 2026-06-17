"""Order views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Order, OrderStatus
from .serializers import OrderSerializer
from apps.users.permissions import IsManager


@extend_schema_view(
    list=extend_schema(description='List user orders'),
    retrieve=extend_schema(description='Get order details'),
    create=extend_schema(description='Create order'),
)
class OrderViewSet(viewsets.ModelViewSet):
    """Order CRUD operations."""
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_manager:
            return Order.objects.select_related('user').prefetch_related('items').all()
        return Order.objects.filter(user=self.request.user).prefetch_related('items')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsManager])
    def cancel(self, request, pk=None):
        """Cancel order."""
        order = self.get_object()
        if order.status == OrderStatus.CANCELLED:
            return Response({'success': False, 'message': 'Order already cancelled'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        order.status = OrderStatus.CANCELLED
        order.save()
        
        return Response({'success': True, 'message': 'Order cancelled successfully'})
