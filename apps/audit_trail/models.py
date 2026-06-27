"""Audit Trail models."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditAction(models.TextChoices):
    """Audit action types."""
    CREATE = 'CREATE', 'Create'
    READ = 'READ', 'Read'
    UPDATE = 'UPDATE', 'Update'
    DELETE = 'DELETE', 'Delete'
    LOGIN = 'LOGIN', 'Login'
    LOGOUT = 'LOGOUT', 'Logout'
    FAILED_LOGIN = 'FAILED_LOGIN', 'Failed Login'
    EXPORT = 'EXPORT', 'Export'
    IMPORT = 'IMPORT', 'Import'
    APPROVE = 'APPROVE', 'Approve'
    REJECT = 'REJECT', 'Reject'
    ESCALATE = 'ESCALATE', 'Escalate'
    ASSIGN = 'ASSIGN', 'Assign'
    RESOLVE = 'RESOLVE', 'Resolve'


class AuditTrail(models.Model):
    """Audit trail model for tracking system activities."""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_trails'
    )
    action = models.CharField(max_length=20, choices=AuditAction.choices)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    
    # Request metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    request_path = models.CharField(max_length=500, null=True, blank=True)
    
    # Changes
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, default='SUCCESS')
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_trails'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
            models.Index(fields=['action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.action} - {self.resource_type} - {self.created_at}"