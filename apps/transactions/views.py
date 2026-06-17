"""Transaction views."""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Transaction
from .serializers import TransactionSerializer


@extend_schema_view(
    list=extend_schema(description='List user transactions'),
    retrieve=extend_schema(description='Get transaction details'),
)
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """Transaction view operations."""
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction_type', 'status']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_manager:
            return Transaction.objects.select_related('user').all()
        return Transaction.objects.filter(user=self.request.user)
