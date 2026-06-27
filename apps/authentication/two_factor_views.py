"""Two-factor authentication views for Django REST Framework."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import (
    TwoFactorSetup, TwoFactorToken, TwoFactorLog, TwoFactorBackupCode,
    TwoFactorMethod as TwoFactorMethodModel
)
from .serializers import (
    TwoFactorSetupSerializer, TwoFactorSetupUpdateSerializer,
    TwoFactorTokenSerializer, TwoFactorBackupCodeSerializer,
    TwoFactorVerifySerializer
)
from apps.users.permissions import IsManagerOrAdmin
from apps.authentication.two_factor import (
    setup_email_2fa, setup_sms_2fa, setup_auth_app_2fa,
    verify_2fa_token, verify_backup_code
)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(description='List 2FA setups'),
    retrieve=extend_schema(description='Get 2FA setup details'),
    update=extend_schema(description='Update 2FA setup'),
    partial_update=extend_schema(description='Partially update 2FA setup'),
)
class TwoFactorSetupViewSet(viewsets.ModelViewSet):
    """Two-factor authentication setup operations."""
    serializer_class = TwoFactorSetupSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_enabled', 'is_required', 'primary_method']
    search_fields = ['user__email', 'user__full_name', 'email']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        return TwoFactorSetup.objects.select_related('user').all()
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def setup_email(self, request, pk=None):
        """Setup email-based 2FA."""
        setup = self.get_object()
        email = request.data.get('email')
        
        if setup.email == email:
            return Response({'success': True, 'message': 'Email already set and verified'})
        
        success, message = setup_email_2fa(setup.user, email)
        
        if success:
            return Response({'success': True, 'message': message})
        else:
            return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def setup_sms(self, request, pk=None):
        """Setup SMS-based 2FA."""
        setup = self.get_object()
        phone_number = request.data.get('phone_number')
        
        if setup.phone_number == phone_number:
            return Response({'success': True, 'message': 'Phone number already set and verified'})
        
        success, message = setup_sms_2fa(setup.user, phone_number)
        
        if success:
            return Response({'success': True, 'message': message})
        else:
            return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def setup_auth_app(self, request, pk=None):
        """Setup authenticator app-based 2FA."""
        setup = self.get_object()
        
        success, data = setup_auth_app_2fa(setup.user)
        
        if success:
            setup.secret_key = data['secret_key']
            setup.recovery_codes = data['recovery_codes']
            setup.save()
            
            return Response({
                'success': True,
                'message': 'Authenticator app setup initiated',
                'qr_url': data['qr_url'],
                'secret_key': data['secret_key'],
                'recovery_codes': data['recovery_codes']
            })
        else:
            return Response({'success': False, 'message': data}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def verify_email(self, request, pk=None):
        """Verify email for 2FA."""
        setup = self.get_object()
        email = request.data.get('email')
        
        if not email:
            return Response({'success': False, 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        setup.email = email
        setup.email_verified = True
        setup.save()
        
        return Response({'success': True, 'message': 'Email verified successfully'})
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def verify_sms(self, request, pk=None):
        """Verify SMS for 2FA."""
        setup = self.get_object()
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({'success': False, 'message': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        setup.phone_number = phone_number
        setup.phone_verified = True
        setup.save()
        
        return Response({'success': True, 'message': 'Phone number verified successfully'})
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def enable_2fa(self, request, pk=None):
        """Enable two-factor authentication."""
        setup = self.get_object()
        
        # Validate setup
        if not setup.email and not setup.phone_number and not setup.secret_key:
            return Response({'success': False, 'message': 'Please setup at least one 2FA method'}, status=status.HTTP_400_BAD_REQUEST)
        
        setup.is_enabled = True
        setup.save()
        
        return Response({'success': True, 'message': '2FA enabled successfully'})
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def disable_2fa(self, request, pk=None):
        """Disable two-factor authentication."""
        setup = self.get_object()
        
        setup.is_enabled = False
        setup.secret_key = None
        setup.recovery_codes = []
        setup.save()
        
        return Response({'success': True, 'message': '2FA disabled successfully'})


@extend_schema_view(
    list=extend_schema(description='List 2FA tokens'),
    create=extend_schema(description='Generate 2FA token'),
)
class TwoFactorTokenViewSet(viewsets.ModelViewSet):
    """Two-factor authentication token operations."""
    serializer_class = TwoFactorTokenSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['method', 'is_used']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return TwoFactorToken.objects.select_related('user').all()
    
    def perform_create(self, serializer):
        pass  # Tokens are generated through other actions
    
    @extend_schema(methods=['post'])
    @action(detail=False, methods=['post'])
    def verify_with_token(self, request):
        """Verify 2FA using token."""
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_id = serializer.validated_data.get('token')
        method = serializer.validated_data['method']
        user = request.user
        
        try:
            token = TwoFactorToken.objects.get(id=token_id, user=user, method=method)
        except TwoFactorToken.DoesNotExist:
            return Response({'success': False, 'message': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        success, message = verify_2fa_token(user, token.token, method)
        
        if success:
            return Response({'success': True, 'message': message})
        else:
            return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(methods=['post'])
    @action(detail=False, methods=['post'])
    def generate_token(self, request):
        """Generate a 2FA token."""
        method = request.data.get('method')
        user = request.user
        
        if method not in TwoFactorMethodModel.values():
            return Response({'success': False, 'message': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)
        
        from .models import TwoFactorToken
        import secrets
        
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        TwoFactorToken.objects.create(
            user=user,
            token=token,
            method=method,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            expires_at=expires_at
        )
        
        return Response({
            'success': True,
            'message': 'Token generated',
            'token': token
        })


@extend_schema_view(
    list=extend_schema(description='List backup codes'),
    create=extend_schema(description='Create backup code'),
)
class TwoFactorBackupCodeViewSet(viewsets.ModelViewSet):
    """Two-factor authentication backup code operations."""
    serializer_class = TwoFactorBackupCodeSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_used']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return TwoFactorBackupCode.objects.select_related('user').all()
    
    @extend_schema(methods=['post'])
    @action(detail=False, methods=['post'])
    def generate_codes(self, request):
        """Generate backup codes."""
        from .models import TwoFactorBackupCode
        from .two_factor import generate_backup_code
        
        count = request.data.get('count', 10)
        user = request.user
        
        # Delete existing backup codes
        TwoFactorBackupCode.objects.filter(user=user).delete()
        
        # Generate new codes
        backup_codes = []
        for _ in range(count):
            code = generate_backup_code()
            backup_codes.append(TwoFactorBackupCode.objects.create(
                user=user,
                code=code
            ))
        
        return Response({
            'success': True,
            'message': f'{count} backup codes generated',
            'backup_codes': [code.code for code in backup_codes]
        })
    
    @extend_schema(methods=['post'])
    @action(detail=False, methods=['post'])
    def use_backup_code(self, request):
        """Use a backup code."""
        code = request.data.get('code')
        user = request.user
        
        success, message = verify_backup_code(user, code)
        
        if success:
            return Response({'success': True, 'message': message})
        else:
            return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Count
from apps.transactions.models import Transaction
from rest_framework import viewsets

@action(detail=False, methods=['get'])
def stats(self, request):
    """Get 2FA statistics."""
    user = request.user
    
    total_users = User.objects.count()
    users_with_2fa = TwoFactorSetup.objects.filter(is_enabled=True).count()
    users_with_2fa_required = TwoFactorSetup.objects.filter(is_required=True).count()
    
    method_stats = TwoFactorSetup.objects.values('primary_method').annotate(
        count=Count('id')
    )
    
    today_tokens = TwoFactorToken.objects.filter(
        created_at__date=timezone.now().date()
    ).count()
    
    return Response({
        'success': True,
        'data': {
            'total_users': total_users,
            'users_with_2fa': users_with_2fa,
            'users_with_2fa_required': users_with_2fa_required,
            '2fa_adoption_rate': round((users_with_2fa / total_users) * 100, 2) if total_users > 0 else 0,
            'method_distribution': list(method_stats),
            'today_tokens_generated': today_tokens,
        }
    })