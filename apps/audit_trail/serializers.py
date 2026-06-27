"""Audit Trail serializers."""
from rest_framework import serializers
from .models import AuditTrail, AuditAction


class AuditTrailSerializer(serializers.ModelSerializer):
    """Audit trail serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditTrail
        fields = [
            'id', 'user', 'user_email', 'user_full_name', 'action',
            'action_display', 'resource_type', 'resource_id', 'description',
            'ip_address', 'user_agent', 'request_method', 'request_path',
            'old_values', 'new_values', 'status', 'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AuditTrailListSerializer(serializers.ModelSerializer):
    """Simplified audit trail serializer for list views."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditTrail
        fields = [
            'id', 'user_email', 'action', 'action_display', 'resource_type',
            'resource_id', 'description', 'status', 'created_at'
        ]