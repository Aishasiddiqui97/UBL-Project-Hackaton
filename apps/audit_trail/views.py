"""Audit Trail views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import AuditTrail
from .serializers import AuditTrailSerializer, AuditTrailListSerializer
from apps.users.permissions import IsManagerOrAdmin


@extend_schema_view(
    list=extend_schema(description='List audit trail entries'),
    retrieve=extend_schema(description='Get audit trail entry details'),
)
class AuditTrailViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit trail operations - read only for compliance."""
    serializer_class = AuditTrailSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['action', 'resource_type', 'status', 'user']
    search_fields = ['description', 'resource_id', 'user__email', 'user__full_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return AuditTrail.objects.select_related('user').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AuditTrailListSerializer
        return AuditTrailSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get audit trail statistics."""
        queryset = self.get_queryset()
        
        total = queryset.count()
        by_action = queryset.values('action').annotate(count=models.Count('id')).order_by('-count')[:10]
        by_resource = queryset.values('resource_type').annotate(count=models.Count('id')).order_by('-count')[:10]
        by_status = queryset.values('status').annotate(count=models.Count('id'))
        by_user = queryset.values('user__email').annotate(count=models.Count('id')).order_by('-count')[:10]
        
        return Response({
            'success': True,
            'data': {
                'total_entries': total,
                'by_action': list(by_action),
                'by_resource_type': list(by_resource),
                'by_status': list(by_status),
                'top_users': list(by_user),
            }
        })
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export audit trail as CSV."""
        import csv
        from django.http import HttpResponse
        
        queryset = self.filter_queryset(self.get_queryset())
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="audit_trail_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'User', 'Action', 'Resource Type', 'Resource ID',
            'Description', 'IP Address', 'Status', 'Created At'
        ])
        
        for entry in queryset[:10000]:
            writer.writerow([
                entry.id,
                entry.user.email if entry.user else 'System',
                entry.action,
                entry.resource_type,
                entry.resource_id or '',
                entry.description,
                entry.ip_address or '',
                entry.status,
                entry.created_at.isoformat(),
            ])
        
        return response