"""Notification services."""
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, NotificationType
from typing import Optional


class NotificationService:
    """Service for managing notifications."""
    
    @staticmethod
    def send_email(to_email: str, subject: str, message: str) -> bool:
        """Send email notification."""
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
    
    @staticmethod
    def create_system_notification(user, subject: str, message: str) -> Optional[Notification]:
        """Create system notification."""
        try:
            return Notification.objects.create(
                user=user,
                notification_type=NotificationType.SYSTEM,
                subject=subject,
                message=message
            )
        except Exception as e:
            print(f"System notification creation failed: {e}")
            return None
