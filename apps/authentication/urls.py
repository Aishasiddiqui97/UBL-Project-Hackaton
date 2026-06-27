"""Two-factor authentication URLs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TwoFactorSetupViewSet, TwoFactorTokenViewSet, TwoFactorBackupCodeViewSet

router = DefaultRouter()
router.register(r'setups', TwoFactorSetupViewSet, basename='two-factor-setup')
router.register(r'tokens', TwoFactorTokenViewSet, basename='two-factor-token')
router.register(r'backup-codes', TwoFactorBackupCodeViewSet, basename='two-factor-backup-code')

urlpatterns = [
    path('', include(router.urls)),
]