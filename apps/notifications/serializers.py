"""Notification serializers."""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer."""
    
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'subject', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
