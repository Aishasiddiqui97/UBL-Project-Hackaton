"""Authentication views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegisterSerializer, LoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .models import PasswordResetToken
from apps.users.serializers import UserSerializer
from apps.notifications.services import NotificationService

User = get_user_model()


class RegisterView(APIView):
    """User registration endpoint."""
    permission_classes = [AllowAny]
    
    @extend_schema(request=RegisterSerializer, responses={201: UserSerializer})
    @method_decorator(ratelimit(key='ip', rate='5/h', method='POST'))
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send welcome email
        NotificationService.send_email(
            user.email,
            'Welcome to Our Platform',
            f'Hello {user.full_name}, welcome to our platform!'
        )
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'data': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User login endpoint."""
    permission_classes = [AllowAny]
    
    @extend_schema(request=LoginSerializer)
    @method_decorator(ratelimit(key='ip', rate='10/h', method='POST'))
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }
        })


class LogoutView(APIView):
    """User logout endpoint."""
    permission_classes = [IsAuthenticated]
    
    @extend_schema(request=None)
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Logout failed',
                'errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """Request password reset endpoint."""
    permission_classes = [AllowAny]
    
    @extend_schema(request=PasswordResetRequestSerializer)
    @method_decorator(ratelimit(key='ip', rate='3/h', method='POST'))
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            reset_token = PasswordResetToken.generate_token(user)
            
            # Send password reset email
            NotificationService.send_email(
                user.email,
                'Password Reset Request',
                f'Use this token to reset your password: {reset_token.token}'
            )
            
            return Response({
                'success': True,
                'message': 'Password reset link sent to your email'
            })
        except User.DoesNotExist:
            # Don't reveal if user exists for security
            return Response({
                'success': True,
                'message': 'If the email exists, a reset link has been sent'
            })


class PasswordResetConfirmView(APIView):
    """Confirm password reset endpoint."""
    permission_classes = [AllowAny]
    
    @extend_schema(request=PasswordResetConfirmSerializer)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_str = serializer.validated_data['token']
        password = serializer.validated_data['password']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token_str)
            
            if not reset_token.is_valid:
                return Response({
                    'success': False,
                    'message': 'Invalid or expired token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            reset_token.is_used = True
            reset_token.save()
            
            return Response({
                'success': True,
                'message': 'Password reset successful'
            })
        except PasswordResetToken.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
