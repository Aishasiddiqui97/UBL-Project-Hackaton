"""Audit Trail admin."""
from django.contrib import admin
from .models import AuditTrail


@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'resource_type', 'resource_id', 'status', 'created_at']
    list_filter = ['action', 'resource_type', 'status', 'created_at']
    search_fields = ['user__email', 'user__full_name', 'resource_id', 'description']
    readonly_fields = [
        'user', 'action', 'resource_type', 'resource_id', 'description',
        'ip_address', 'user_agent', 'request_method', 'request_path',
        'old_values', 'new_values', 'status', 'error_message', 'created_at'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False