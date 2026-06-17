"""Payment views."""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Payment
from .serializers import PaymentSerializer


@extend_schema_view(
    list=extend_schema(description='List user payments'),
    retrieve=extend_schema(description='Get payment details'),
)
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Payment view operations."""
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'method']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_manager:
            return Payment.objects.select_related('user', 'order').all()
        return Payment.objects.filter(user=self.request.user).select_related('order')
