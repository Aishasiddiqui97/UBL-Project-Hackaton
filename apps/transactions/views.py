"""Transaction views."""
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema
from .models import Transaction, FraudAlert
from .serializers import TransactionSerializer, TransactionListSerializer, FraudAlertSerializer
from apps.users.permissions import IsManagerOrAdmin
import uuid
from decimal import Decimal


class TransactionViewSet(ModelViewSet):
    """Transaction viewset with CRUD operations."""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['transaction_type', 'status', 'risk_level']
    search_fields = ['reference', 'account_number', 'description']
    ordering_fields = ['created_at', 'amount', 'fraud_probability']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter transactions based on user role."""
        user = self.request.user
        if user.is_admin or user.is_manager:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)
    
    def get_serializer_class(self):
        """Use list serializer for list action."""
        if self.action == 'list':
            return TransactionListSerializer
        return TransactionSerializer
    
    def perform_create(self, serializer):
        """Create transaction with auto-generated reference."""
        # Generate unique reference
        reference = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # Get IP address from request
        ip_address = self.request.META.get('REMOTE_ADDR')
        
        serializer.save(
            user=self.request.user,
            reference=reference,
            ip_address=ip_address
        )
    
    @extend_schema(methods=['get'])
    @action(detail=False, methods=['get'])
    def suspicious(self, request):
        """Get suspicious transactions."""
        queryset = self.get_queryset().filter(
            risk_level__in=['MEDIUM', 'HIGH'],
            status__in=['FLAGGED', 'UNDER_REVIEW']
        )
        
        serializer = TransactionListSerializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Suspicious transactions retrieved',
            'data': serializer.data
        })
    
    @extend_schema(methods=['get'])
    @action(detail=False, methods=['get'])
    def fraud_stats(self, request):
        """Get fraud detection statistics."""
        queryset = self.get_queryset()
        
        total = queryset.count()
        flagged = queryset.filter(status='FLAGGED').count()
        under_review = queryset.filter(status='UNDER_REVIEW').count()
        clear = queryset.filter(status='CLEAR').count()
        
        high_risk = queryset.filter(risk_level='HIGH').count()
        medium_risk = queryset.filter(risk_level='MEDIUM').count()
        low_risk = queryset.filter(risk_level='LOW').count()
        
        return Response({
            'success': True,
            'data': {
                'total_transactions': total,
                'status_breakdown': {
                    'flagged': flagged,
                    'under_review': under_review,
                    'clear': clear
                },
                'risk_breakdown': {
                    'high_risk': high_risk,
                    'medium_risk': medium_risk,
                    'low_risk': low_risk
                }
            }
        })


class FraudAlertViewSet(ModelViewSet):
    """Fraud alert viewset."""
    serializer_class = FraudAlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['alert_type', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter alerts based on user role."""
        user = self.request.user
        if user.is_admin or user.is_manager:
            return FraudAlert.objects.all()
        return FraudAlert.objects.filter(transaction__user=user)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'], permission_classes=[IsManagerOrAdmin])
    def resolve(self, request, pk=None):
        """Resolve fraud alert."""
        alert = self.get_object()
        alert.status = 'RESOLVED'
        alert.save()
        
        # Also update transaction status
        alert.transaction.status = 'CLEAR'
        alert.transaction.save()
        
        return Response({
            'success': True,
            'message': 'Alert resolved successfully'
        })
