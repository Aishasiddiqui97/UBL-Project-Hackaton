"""Compliance views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.db.models import Count, Avg
from django.utils import timezone
from .models import ComplianceRule, ComplianceCheck, ComplianceReport
from .serializers import (
    ComplianceRuleSerializer, ComplianceCheckSerializer,
    ComplianceReportSerializer, ComplianceCheckCreateSerializer
)
from apps.users.permissions import IsManagerOrAdmin


@extend_schema_view(
    list=extend_schema(description='List compliance rules'),
    retrieve=extend_schema(description='Get compliance rule details'),
    create=extend_schema(description='Create compliance rule'),
    update=extend_schema(description='Update compliance rule'),
)
class ComplianceRuleViewSet(viewsets.ModelViewSet):
    """Compliance rule management."""
    serializer_class = ComplianceRuleSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['regulation_type', 'severity', 'is_active']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['severity', 'created_at']
    ordering = ['-severity', 'code']
    
    def get_queryset(self):
        return ComplianceRule.objects.all()


@extend_schema_view(
    list=extend_schema(description='List compliance checks'),
    retrieve=extend_schema(description='Get compliance check details'),
    create=extend_schema(description='Create compliance check'),
)
class ComplianceCheckViewSet(viewsets.ModelViewSet):
    """Compliance check operations."""
    serializer_class = ComplianceCheckSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'rule', 'passed']
    search_fields = ['transaction_id', 'user_id', 'account_number']
    ordering_fields = ['checked_at', 'score']
    ordering = ['-checked_at']
    
    def get_queryset(self):
        return ComplianceCheck.objects.select_related('rule', 'checked_by', 'reviewed_by').all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ComplianceCheckCreateSerializer
        return ComplianceCheckSerializer
    
    def perform_create(self, serializer):
        serializer.save(checked_by=self.request.user)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Review compliance check."""
        check = self.get_object()
        review_notes = request.data.get('review_notes', '')
        new_status = request.data.get('status')
        
        if new_status and new_status not in ComplianceCheck.Status.values:
            return Response({'success': False, 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_status:
            check.status = new_status
        check.reviewed_by = request.user
        check.reviewed_at = timezone.now()
        check.review_notes = review_notes
        check.save()
        
        return Response({'success': True, 'message': 'Check reviewed'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get compliance statistics."""
        queryset = self.get_queryset()
        
        total = queryset.count()
        passed = queryset.filter(passed=True).count()
        failed = queryset.filter(passed=False).count()
        pending = queryset.filter(status=ComplianceCheck.Status.PENDING_REVIEW).count()
        
        avg_score = queryset.aggregate(avg=Avg('score'))['avg'] or 0
        
        by_status = queryset.values('status').annotate(count=Count('id'))
        by_regulation = queryset.values('rule__regulation_type').annotate(count=Count('id'))
        by_rule = queryset.values('rule__code').annotate(count=Count('id'), avg_score=Avg('score')).order_by('-count')[:10]
        
        return Response({
            'success': True,
            'data': {
                'total_checks': total,
                'passed': passed,
                'failed': failed,
                'pending_review': pending,
                'average_score': round(avg_score, 2),
                'by_status': list(by_status),
                'by_regulation_type': list(by_regulation),
                'top_rules': list(by_rule),
            }
        })


@extend_schema_view(
    list=extend_schema(description='List compliance reports'),
    retrieve=extend_schema(description='Get compliance report details'),
    create=extend_schema(description='Create compliance report'),
)
class ComplianceReportViewSet(viewsets.ModelViewSet):
    """Compliance report management."""
    serializer_class = ComplianceReportSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['report_type', 'status']
    search_fields = ['report_number', 'title', 'description']
    ordering_fields = ['prepared_at', 'period_start']
    ordering = ['-prepared_at']
    
    def get_queryset(self):
        return ComplianceReport.objects.select_related('prepared_by', 'approved_by').all()
    
    def perform_create(self, serializer):
        serializer.save(prepared_by=self.request.user)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve compliance report."""
        report = self.get_object()
        report.status = ComplianceReport.Status.APPROVED
        report.approved_by = request.user
        report.approved_at = timezone.now()
        report.save()
        return Response({'success': True, 'message': 'Report approved'})
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def file_report(self, request, pk=None):
        """File compliance report."""
        report = self.get_object()
        report.status = ComplianceReport.Status.FILED
        report.filed_at = timezone.now()
        report.save()
        return Response({'success': True, 'message': 'Report filed'})