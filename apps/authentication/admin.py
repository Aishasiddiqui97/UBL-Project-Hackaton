"""Authentication admin."""
from django.contrib import admin
from .models import RefreshToken, PasswordResetToken


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    """Refresh token admin."""
    list_display = ['user', 'is_blacklisted', 'created_at', 'expires_at']
    list_filter = ['is_blacklisted', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'expires_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Password reset token admin."""
    list_display = ['user', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'expires_at']
