"""Authentication views - JWT Login/Logout and Two-Factor."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from .models import TwoFactorSetup, TwoFactorToken, TwoFactorLog, TwoFactorBackupCode, TwoFactorMethod
from .serializers import (
    TwoFactorSetupSerializer, TwoFactorSetupUpdateSerializer,
    TwoFactorTokenSerializer, TwoFactorBackupCodeSerializer,
    TwoFactorVerifySerializer
)
from apps.users.permissions import IsManagerOrAdmin
from apps.users.serializers import UserSerializer

User = get_user_model()


class LoginView(APIView):
    """Login with email and password to get JWT tokens."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'success': False,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Serialize user data
        user_serializer = UserSerializer(user)

        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user_serializer.data
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logout by blacklisting the refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(description='List 2FA setups'),
    retrieve=extend_schema(description='Get 2FA setup details'),
    create=extend_schema(description='Create 2FA setup'),
    update=extend_schema(description='Update 2FA setup'),
)
class TwoFactorSetupViewSet(viewsets.ModelViewSet):
    """Two-factor authentication setup operations."""
    serializer_class = TwoFactorSetupSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_enabled', 'is_required', 'primary_method']
    search_fields = ['user__email', 'user__full_name', 'email']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return TwoFactorSetup.objects.select_related('user').all()
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        """Enable two-factor authentication."""
        setup = self.get_object()
        method = request.data.get('method')
        
        if method not in TwoFactorMethod.values:
            return Response({'success': False, 'message': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)
        
        setup.is_enabled = True
        setup.primary_method = method
        setup.save()
        
        return Response({'success': True, 'message': '2FA enabled successfully'})
    
    @extend_schema(methods=['post'])
    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        """Disable two-factor authentication."""
        setup = self.get_object()
        setup.is_enabled = False
        setup.save()
        
        # Log the action
        TwoFactorLog.objects.create(
            user=setup.user,
            action='disable',
            method=setup.primary_method,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'success': True, 'message': '2FA disabled successfully'})
    
    @action(detail=True, methods=['get'])
    def generate_backup_codes(self, request, pk=None):
        """Generate backup codes for 2FA."""
        from django.db import transaction
        import random
        import string
        
        setup = self.get_object()
        
        with transaction.atomic():
            # Delete existing backup codes
            TwoFactorBackupCode.objects.filter(user=setup.user).delete()
            
            # Generate 10 new backup codes
            backup_codes = []
            for _ in range(10):
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                backup_codes.append(TwoFactorBackupCode.objects.create(
                    user=setup.user,
                    code=code
                ))
        
        # Update setup with recovery codes for apps
        app_codes = [code.code for code in backup_codes]
        if not setup.recovery_codes:
            setup.recovery_codes = []
        setup.recovery_codes.extend(app_codes)
        setup.save()
        
        return Response({
            'success': True,
            'message': 'Backup codes generated',
            'backup_codes': app_codes
        })


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
        token_data = serializer.validated_data
        user = token_data['user']
        
        # Generate token
        import secrets
        token = secrets.token_urlsafe(32)
        
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        TwoFactorToken.objects.create(
            user=user,
            token=token,
            method=token_data['method'],
            ip_address=serializer.context['request'].META.get('REMOTE_ADDR'),
            user_agent=serializer.context['request'].META.get('HTTP_USER_AGENT', ''),
            device=serializer.context['request'].META.get('HTTP_USER_AGENT', '').split('/')[0] if serializer.context['request'].META.get('HTTP_USER_AGENT') else None,
            expires_at=expires_at
        )
        
        # Log token creation
        TwoFactorLog.objects.create(
            user=user,
            action='token_generated',
            method=token_data['method'],
            ip_address=serializer.context['request'].META.get('REMOTE_ADDR'),
            user_agent=serializer.context['request'].META.get('HTTP_USER_AGENT', '')
        )
    
    @extend_schema(methods=['post'])
    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify 2FA token."""
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        method = serializer.validated_data['method']
        user = request.user
        
        # Create a new token based on the method
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        token = secrets.token_urlsafe(32)
        
        two_factor_token = TwoFactorToken.objects.create(
            user=user,
            token=token,
            method=method,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            expires_at=expires_at
        )
        
        # Method-specific processing
        if method == TwoFactorMethod.EMAIL:
            email = serializer.validated_data.get('email')
            if email:
                send_mail(
                    'Two-Factor Authentication Code',
                    f'Your 2FA code is: {token}',
                    'no-reply@example.com',
                    [email]
                )
        
        elif method == TwoFactorMethod.SMS:
            phone = serializer.validated_data.get('phone')
            if phone:
                # In production, use an SMS service
                pass
        
        return Response({
            'success': True,
            'message': '2FA verification initiated',
            'token_id': two_factor_token.id,
            'method': method
        })
    
    @action(detail=True, methods=['post'])
    def verify_token(self, request, pk=None):
        """Verify a specific 2FA token."""
        token = self.get_object()
        
        if token.is_used:
            return Response({'success': False, 'message': 'Token has already been used'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > token.expires_at:
            return Response({'success': False, 'message': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify token (in real implementation, validate token against stored hash)
        token.is_used = True
        token.used_at = timezone.now()
        token.save()
        
        # Log verification
        TwoFactorLog.objects.create(
            user=token.user,
            action='success',
            method=token.method,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'success': True,
            'message': 'Token verified successfully'
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
    
    @action(detail=False, methods=['post'])
    def use_backup_code(self, request):
        """Use a backup code to authenticate."""
        code = request.data.get('code')
        user = request.user
        
        try:
            backup_code = TwoFactorBackupCode.objects.get(code=code, is_used=False)
        except TwoFactorBackupCode.DoesNotExist:
            return Response({'success': False, 'message': 'Invalid or used backup code'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as used
        backup_code.is_used = True
        backup_code.used_at = timezone.now()
        backup_code.save()
        
        # Log usage
        TwoFactorLog.objects.create(
            user=user,
            action='backup_code_used',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'success': True,
            'message': 'Backup code used successfully'
        })


@action(detail=False, methods=['get'])
def stats(self, request):
    """Get 2FA statistics."""
    user = request.user
    
    total_users = User.objects.count()
    users_with_2fa = TwoFactorSetup.objects.filter(is_enabled=True).count()
    users_with_2fa_required = TwoFactorSetup.objects.filter(is_required=True).count()
    
    method_stats = TwoFactorSetup.objects.values('primary_method').annotate(
        count=models.Count('id')
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