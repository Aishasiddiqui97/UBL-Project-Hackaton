"""KYC views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.db.models import Count, Q
from django.utils import timezone
from .models import KYCProfile, KYCDocument, KYCCheck
from .serializers import (
    KYCProfileSerializer, KYCProfileListSerializer, KYCProfileCreateSerializer,
    KYCDocumentSerializer, KYCDocumentUploadSerializer,
    KYCCheckSerializer, KYCReviewSerializer
)
from apps.users.permissions import IsManagerOrAdmin


@extend_schema_view(
    list=extend_schema(description='List KYC profiles'),
    retrieve=extend_schema(description='Get KYC profile details'),
    create=extend_schema(description='Create KYC profile'),
    update=extend_schema(description='Update KYC profile'),
    partial_update=extend_schema(description='Partially update KYC profile'),
)
class KYCProfileViewSet(viewsets.ModelViewSet):
    """KYC profile management."""
    serializer_class = KYCProfileSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'risk_rating', 'nationality', 'country_of_residence']
    search_fields = ['user__email', 'user__full_name', 'full_name', 'id_document_number']
    ordering_fields = ['created_at', 'submitted_at', 'approved_at', 'status', 'risk_rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return KYCProfile.objects.select_related('user', 'reviewed_by').prefetch_related('documents', 'checks').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return KYCProfileListSerializer
        elif self.action == 'create':
            return KYCProfileCreateSerializer
        return KYCProfileSerializer
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Review KYC profile - approve/reject/require update."""
        profile = self.get_object()
        serializer = KYCReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_status = serializer.validated_data['status']
        review_notes = serializer.validated_data.get('review_notes', '')
        rejection_reason = serializer.validated_data.get('rejection_reason', '')
        risk_rating = serializer.validated_data.get('risk_rating')
        expires_at = serializer.validated_data.get('expires_at')
        
        profile.status = new_status
        profile.reviewed_by = request.user
        profile.reviewed_at = timezone.now()
        profile.review_notes = review_notes
        
        if new_status == KYCProfile.Status.APPROVED:
            profile.approved_at = timezone.now()
            if expires_at:
                profile.expires_at = expires_at
            else:
                # Default expiry: 1 year
                profile.expires_at = timezone.now() + timezone.timedelta(days=365)
        elif new_status == KYCProfile.Status.REJECTED:
            profile.rejection_reason = rejection_reason
        elif new_status == KYCProfile.Status.REQUIRES_UPDATE:
            pass
        
        if risk_rating:
            profile.risk_rating = risk_rating
        
        profile.save()
        
        # Create audit trail
        from apps.audit_trail.models import AuditTrail, AuditAction
        AuditTrail.objects.create(
            user=request.user,
            action=AuditAction.APPROVE if new_status == KYCProfile.Status.APPROVED else AuditAction.REJECT,
            resource_type='KYCProfile',
            resource_id=str(profile.id),
            description=f"KYC profile {new_status.lower()} for user {profile.user.email}",
            new_values={'status': new_status, 'risk_rating': profile.risk_rating},
            status='SUCCESS'
        )
        
        return Response({
            'success': True,
            'message': f'KYC profile {new_status.lower()} successfully',
            'data': KYCProfileSerializer(profile).data
        })
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        """Upload document to KYC profile."""
        profile = self.get_object()
        serializer = KYCDocumentUploadSerializer(data=request.data, context={'kyc_profile_id': profile.id})
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        return Response({
            'success': True,
            'message': 'Document uploaded successfully',
            'data': KYCDocumentSerializer(document).data
        })
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Get KYC profile documents."""
        profile = self.get_object()
        documents = profile.documents.all()
        serializer = KYCDocumentSerializer(documents, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    @action(detail=True, methods=['get'])
    def checks(self, request, pk=None):
        """Get KYC profile checks."""
        profile = self.get_object()
        checks = profile.checks.all()
        serializer = KYCCheckSerializer(checks, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get KYC statistics."""
        queryset = self.get_queryset()
        
        total = queryset.count()
        pending = queryset.filter(status=KYCProfile.Status.PENDING_REVIEW).count()
        in_progress = queryset.filter(status=KYCProfile.Status.IN_PROGRESS).count()
        approved = queryset.filter(status=KYCProfile.Status.APPROVED).count()
        rejected = queryset.filter(status=KYCProfile.Status.REJECTED).count()
        expired = queryset.filter(status=KYCProfile.Status.EXPIRED).count()
        requires_update = queryset.filter(status=KYCProfile.Status.REQUIRES_UPDATE).count()
        
        by_risk = queryset.values('risk_rating').annotate(count=Count('id'))
        by_nationality = queryset.values('nationality').annotate(count=Count('id')).order_by('-count')[:10]
        by_status = queryset.values('status').annotate(count=Count('id'))
        
        # Expiring soon (within 30 days)
        expiring_soon = queryset.filter(
            status=KYCProfile.Status.APPROVED,
            expires_at__lte=timezone.now() + timezone.timedelta(days=30),
            expires_at__gt=timezone.now()
        ).count()
        
        return Response({
            'success': True,
            'data': {
                'total_profiles': total,
                'pending_review': pending,
                'in_progress': in_progress,
                'approved': approved,
                'rejected': rejected,
                'expired': expired,
                'requires_update': requires_update,
                'expiring_soon': expiring_soon,
                'by_risk_rating': list(by_risk),
                'by_nationality': list(by_nationality),
                'by_status': list(by_status),
            }
        })
    
    @action(detail=False, methods=['get'])
    def my_kyc(self, request):
        """Get current user's KYC profile."""
        try:
            profile = KYCProfile.objects.get(user=request.user)
            serializer = KYCProfileSerializer(profile)
            return Response({'success': True, 'data': serializer.data})
        except KYCProfile.DoesNotExist:
            return Response({'success': False, 'message': 'KYC profile not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    list=extend_schema(description='List KYC documents'),
    create=extend_schema(description='Upload KYC document'),
)
class KYCDocumentViewSet(viewsets.ModelViewSet):
    """KYC document operations."""
    serializer_class = KYCDocumentSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['document_type', 'is_verified']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        return KYCDocument.objects.select_related('kyc_profile', 'verified_by').all()
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify KYC document."""
        document = self.get_object()
        is_verified = request.data.get('is_verified', True)
        verification_notes = request.data.get('verification_notes', '')
        
        document.is_verified = is_verified
        document.verified_by = request.user
        document.verified_at = timezone.now()
        document.verification_notes = verification_notes
        document.save()
        
        return Response({'success': True, 'message': 'Document verified'})


@extend_schema_view(
    list=extend_schema(description='List KYC checks'),
)
class KYCCheckViewSet(viewsets.ModelViewSet):
    """KYC check operations."""
    serializer_class = KYCCheckSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['check_type', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return KYCCheck.objects.select_related('kyc_profile', 'reviewed_by').all()
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Review KYC check."""
        check = self.get_object()
        new_status = request.data.get('status')
        review_notes = request.data.get('review_notes', '')
        
        if new_status not in KYCCheck.Status.values:
            return Response({'success': False, 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        check.status = new_status
        check.reviewed_by = request.user
        check.reviewed_at = timezone.now()
        check.review_notes = review_notes
        if new_status in ['PASSED', 'FAILED']:
            check.completed_at = timezone.now()
        check.save()
        
        return Response({'success': True, 'message': 'Check reviewed'})