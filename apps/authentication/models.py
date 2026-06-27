"""Two-factor authentication models."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TwoFactorMethod(models.TextChoices):
    """Two-factor authentication method choices."""
    EMAIL = 'EMAIL', 'Email'
    SMS = 'SMS', 'SMS'
    AUTH_APP = 'AUTH_APP', 'Authenticator App'
    BACKUP_CODE = 'BACKUP_CODE', 'Backup Code'
    HARDWARE_KEY = 'HARDWARE_KEY', 'Hardware Key'


class TwoFactorSetup(models.Model):
    """Two-factor authentication setup for users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor_setup')
    
    # Method preferences
    primary_method = models.CharField(max_length=20, choices=TwoFactorMethod.choices, default=TwoFactorMethod.AUTH_APP)
    backup_methods = models.JSONField(default=list)  # Store list of backup method types
    
    # Settings
    is_enabled = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    
    # Email method
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    
    # SMS method
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    
    # Authenticator app
    secret_key = models.CharField(max_length=255, null=True, blank=True)
    recovery_codes = models.JSONField(default=list, null=True, blank=True)
    
    # Hardware key (simplified)
    hardware_key_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Timing
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    # Methods
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'two_factor_setups'
    
    def __str__(self) -> str:
        return f"2FA - {self.user.email} - {self.primary_method}"


class TwoFactorToken(models.Model):
    """Two-factor authentication token for verification."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='two_factor_tokens')
    
    # Token details
    token = models.CharField(max_length=255)
    method = models.CharField(max_length=20, choices=TwoFactorMethod.choices)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'two_factor_tokens'
        indexes = [
            models.Index(fields=['user', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self) -> str:
        return f"Token {self.token[:8]}... - {self.method} - {self.user.email}"


class TwoFactorLog(models.Model):
    """Logging for two-factor authentication attempts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='two_factor_logs')
    
    # Attempt details
    action = models.CharField(max_length=50)  # attempt, success, failure, verify
    method = models.CharField(max_length=20, choices=TwoFactorMethod.choices, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Error/Failure details
    error_message = models.TextField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'two_factor_logs'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self) -> str:
        return f"Log - {self.action} - {self.user.email} - {self.created_at}"


class TwoFactorBackupCode(models.Model):
    """Backup codes for two-factor authentication."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backup_codes')
    
    code = models.CharField(max_length=10)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'two_factor_backup_codes'
        unique_together = [('user', 'code')]
    
    def __str__(self) -> str:
        return f"Backup Code: {self.code} - {self.user.email}"