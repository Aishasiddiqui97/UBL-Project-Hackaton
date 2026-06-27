"""KYC URLs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KYCProfileViewSet, KYCDocumentViewSet, KYCCheckViewSet

router = DefaultRouter()
router.register(r'profiles', KYCProfileViewSet, basename='kyc-profile')
router.register(r'documents', KYCDocumentViewSet, basename='kyc-document')
router.register(r'checks', KYCCheckViewSet, basename='kyc-check')

urlpatterns = [
    path('', include(router.urls)),
]