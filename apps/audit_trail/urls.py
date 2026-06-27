"""Audit Trail URLs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditTrailViewSet

router = DefaultRouter()
router.register(r'', AuditTrailViewSet, basename='audit-trail')

urlpatterns = [
    path('', include(router.urls)),
]