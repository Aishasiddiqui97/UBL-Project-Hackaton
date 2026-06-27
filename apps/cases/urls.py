"""Cases URLs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, CaseCommentViewSet, CaseDocumentViewSet

router = DefaultRouter()
router.register(r'', CaseViewSet, basename='case')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:case_pk>/comments/', CaseCommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='case-comments'),
    path('<int:case_pk>/comments/<int:pk>/', CaseCommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='case-comment-detail'),
    path('<int:case_pk>/documents/', CaseDocumentViewSet.as_view({'get': 'list', 'post': 'create'}), name='case-documents'),
    path('<int:case_pk>/documents/<int:pk>/', CaseDocumentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='case-document-detail'),
]