"""Authentication models."""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class RefreshToken(models.Model):
    """Refresh token model for JWT token management."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=500, unique=True)
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'refresh_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_blacklisted']),
        ]
    
    def __str__(self) -> str:
        return f"Token for {self.user.email}"
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return timezone.now() > self.expires_at


class PasswordResetToken(models.Model):
    """Password reset token model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_used']),
        ]
    
    def __str__(self) -> str:
        return f"Password reset for {self.user.email}"
    
    @classmethod
    def generate_token(cls, user: User) -> 'PasswordResetToken':
        """Generate a password reset token."""
        token = get_random_string(64)
        expires_at = timezone.now() + timedelta(hours=1)
        return cls.objects.create(user=user, token=token, expires_at=expires_at)
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if token is valid."""
        return not self.is_used and not self.is_expired
