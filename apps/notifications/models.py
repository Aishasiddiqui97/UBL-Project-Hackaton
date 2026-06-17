"""Notification models."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationType(models.TextChoices):
    """Notification type choices."""
    EMAIL = 'EMAIL', 'Email'
    SYSTEM = 'SYSTEM', 'System'


class Notification(models.Model):
    """Notification model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.subject} - {self.user.email}"
