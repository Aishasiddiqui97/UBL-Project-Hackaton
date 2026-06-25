"""Transaction URLs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, FraudAlertViewSet

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')
router.register(r'fraud-alerts', FraudAlertViewSet, basename='fraud-alert')

urlpatterns = [
    path('', include(router.urls)),
]
