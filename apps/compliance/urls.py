"""Compliance URLs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplianceRuleViewSet, ComplianceCheckViewSet, ComplianceReportViewSet

router = DefaultRouter()
router.register(r'rules', ComplianceRuleViewSet, basename='compliance-rule')
router.register(r'checks', ComplianceCheckViewSet, basename='compliance-check')
router.register(r'reports', ComplianceReportViewSet, basename='compliance-report')

urlpatterns = [
    path('', include(router.urls)),
]