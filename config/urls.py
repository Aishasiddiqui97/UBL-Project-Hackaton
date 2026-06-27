"""URL configuration for backend project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_root(request):
    """API root endpoint showing available endpoints."""
    return JsonResponse({
        'message': 'Welcome to Backend API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': '/api/auth/',
            'users': '/api/users/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'payments': '/api/payments/',
            'transactions': '/api/transactions/',
            'notifications': '/api/notifications/',
            'kyc': '/api/kyc/',
            'cases': '/api/cases/',
            'compliance': '/api/compliance/',
            'audit_trail': '/api/audit-trail/',
            'documentation': '/api/docs/',
            'admin': '/admin/'
        }
    })

def root_redirect(request):
    """Redirect root URL to API docs."""
    return redirect('/api/docs/')

def health_check(request):
    """Health check endpoint."""
    return JsonResponse({
        'status': 'OK',
        'message': 'Backend API is running',
        'version': '1.0.0'
    })

urlpatterns = [
    # Root URL redirect
    path('', root_redirect, name='root-redirect'),
    
    # Health check
    path('health/', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    
    # New apps
    path('api/kyc/', include('apps.kyc.urls')),
    path('api/cases/', include('apps.cases.urls')),
    path('api/compliance/', include('apps.compliance.urls')),
    path('api/audit-trail/', include('apps.audit_trail.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
