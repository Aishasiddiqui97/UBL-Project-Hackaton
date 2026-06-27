"""Authentication URLs - JWT Login/Logout and Two-Factor."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView, 
    LogoutView,
    TwoFactorSetupViewSet, 
    TwoFactorTokenViewSet, 
    TwoFactorBackupCodeViewSet
)

router = DefaultRouter()
router.register(r'setups', TwoFactorSetupViewSet, basename='two-factor-setup')
router.register(r'tokens', TwoFactorTokenViewSet, basename='two-factor-token')
router.register(r'backup-codes', TwoFactorBackupCodeViewSet, basename='two-factor-backup-code')

urlpatterns = [
    # JWT Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Two-Factor Authentication
    path('', include(router.urls)),
]
