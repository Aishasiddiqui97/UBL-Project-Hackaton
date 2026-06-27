"""Cases views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Case, CaseComment, CaseDocument
from .serializers import (
    CaseSerializer, CaseListSerializer, CaseCreateSerializer,
    CaseCommentSerializer, CaseDocumentSerializer
)
from apps.users.permissions import IsManagerOrAdmin


@extend_schema_view(
    list=extend_schema(description='List cases'),
    retrieve=extend_schema(description='Get case details'),
    create=extend_schema(description='Create a new case'),
    update=extend_schema(description='Update case'),
    partial_update=extend_schema(description='Partially update case'),
)
class CaseViewSet(viewsets.ModelViewSet):
    """Case management operations."""
    serializer_class = CaseSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority', 'case_type', 'assigned_to']
    search_fields = ['case_number', 'title', 'description', 'related_transaction_id']
    ordering_fields = ['opened_at', 'priority', 'due_date']
    ordering = ['-opened_at']
    
    def get_queryset(self):
        return Case.objects.select_related('assigned_to', 'created_by').prefetch_related('comments', 'documents').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CaseListSerializer
        elif self.action == 'create':
            return CaseCreateSerializer
        return CaseSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign case to user."""
        case = self.get_object()
        user_id = request.data.get('user_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
            case.assigned_to = user
            case.status = Case.Status.IN_PROGRESS
            case.save()
            return Response({'success': True, 'message': 'Case assigned successfully'})
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update case status."""
        case = self.get_object()
        new_status = request.data.get('status')
        resolution = request.data.get('resolution', '')
        resolution_summary = request.data.get('resolution_summary', '')
        
        if new_status not in Case.Status.values:
            return Response({'success': False, 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        case.status = new_status
        if resolution:
            case.resolution = resolution
        if resolution_summary:
            case.resolution_summary = resolution_summary
        case.save()
        
        return Response({'success': True, 'message': 'Status updated successfully'})
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add comment to case."""
        case = self.get_object()
        content = request.data.get('content')
        is_internal = request.data.get('is_internal', True)
        
        if not content:
            return Response({'success': False, 'message': 'Content required'}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = CaseComment.objects.create(
            case=case,
            author=request.user,
            content=content,
            is_internal=is_internal
        )
        
        return Response({
            'success': True,
            'message': 'Comment added',
            'data': CaseCommentSerializer(comment).data
        })
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        """Upload document to case."""
        case = self.get_object()
        file = request.FILES.get('file')
        description = request.data.get('description', '')
        
        if not file:
            return Response({'success': False, 'message': 'File required'}, status=status.HTTP_400_BAD_REQUEST)
        
        document = CaseDocument.objects.create(
            case=case,
            uploaded_by=request.user,
            file=file,
            filename=file.name,
            file_size=file.size,
            content_type=file.content_type,
            description=description
        )
        
        return Response({
            'success': True,
            'message': 'Document uploaded',
            'data': CaseDocumentSerializer(document).data
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get case statistics."""
        queryset = self.get_queryset()
        
        total = queryset.count()
        open_cases = queryset.filter(status=Case.Status.OPEN).count()
        in_progress = queryset.filter(status=Case.Status.IN_PROGRESS).count()
        resolved = queryset.filter(status=Case.Status.RESOLVED).count()
        closed = queryset.filter(status=Case.Status.CLOSED).count()
        escalated = queryset.filter(status=Case.Status.ESCALATED).count()
        
        by_priority = queryset.values('priority').annotate(count=models.Count('id'))
        by_type = queryset.values('case_type').annotate(count=models.Count('id'))
        by_assignee = queryset.filter(assigned_to__isnull=False).values('assigned_to__email').annotate(count=models.Count('id')).order_by('-count')[:10]
        
        overdue = queryset.filter(
            due_date__lt=timezone.now(),
            status__in=[Case.Status.OPEN, Case.Status.IN_PROGRESS, Case.Status.UNDER_REVIEW]
        ).count()
        
        return Response({
            'success': True,
            'data': {
                'total_cases': total,
                'open_cases': open_cases,
                'in_progress': in_progress,
                'resolved': resolved,
                'closed': closed,
                'escalated': escalated,
                'overdue': overdue,
                'by_priority': list(by_priority),
                'by_type': list(by_type),
                'by_assignee': list(by_assignee),
            }
        })
    
    @action(detail=False, methods=['get'])
    def my_cases(self, request):
        """Get cases assigned to current user."""
        queryset = self.get_queryset().filter(assigned_to=request.user)
        serializer = CaseListSerializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


@extend_schema_view(
    list=extend_schema(description='List case comments'),
    create=extend_schema(description='Add comment to case'),
)
class CaseCommentViewSet(viewsets.ModelViewSet):
    """Case comment operations."""
    serializer_class = CaseCommentSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseComment.objects.filter(case_id=case_id).select_related('author')
    
    def perform_create(self, serializer):
        case_id = self.kwargs.get('case_pk')
        serializer.save(author=self.request.user, case_id=case_id)


@extend_schema_view(
    list=extend_schema(description='List case documents'),
    create=extend_schema(description='Upload document to case'),
)
class CaseDocumentViewSet(viewsets.ModelViewSet):
    """Case document operations."""
    serializer_class = CaseDocumentSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseDocument.objects.filter(case_id=case_id).select_related('uploaded_by')
    
    def perform_create(self, serializer):
        case_id = self.kwargs.get('case_pk')
        file = self.check_file = self.request.FILES.get('file')
        serializer.save(
            uploaded_by=self.request.user,
            case_id=case_id,
            filename=file.name if file else '',
            file_size=file.size if file else 0,
            content_type=file.content_type if file else ''
        )