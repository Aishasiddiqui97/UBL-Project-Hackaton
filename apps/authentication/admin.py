"""Two-factor authentication admin."""
from django.contrib import admin
from .models import TwoFactorSetup, TwoFactorToken, TwoFactorLog, TwoFactorBackupCode


@admin.register(TwoFactorSetup)
class TwoFactorSetupAdmin(admin.ModelAdmin):
    list_display = ['user', 'primary_method', 'is_enabled', 'is_required', 'last_used_at', 'created_at']
    list_filter = ['is_enabled', 'is_required', 'primary_method', 'created_at']
    search_fields = ['user__email', 'user__full_name', 'email', 'phone_number']
    readonly_fields = ['user', 'created_at', 'updated_at']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Primary Method', {
            'fields': ('primary_method', 'is_enabled', 'is_required')
        }),
        ('Email Method', {
            'fields': ('email_verified', 'email')
        }),
        ('SMS Method', {
            'fields': ('phone_number', 'phone_verified')
        }),
        ('Authenticator App', {
            'fields': ('secret_key', 'recovery_codes')
        }),
        ('Hardware Key', {
            'fields': ('hardware_key_id',)
        }),
        ('Timing', {
            'fields': ('last_used_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(TwoFactorToken)
class TwoFactorTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'method', 'is_used', 'created_at', 'expires_at', 'is_expired']
    list_filter = ['method', 'is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['user', 'token', 'method', 'ip_address', 'user_agent', 'device', 'created_at', 'expires_at', 'used_at']
    
    def is_expired(self, obj):
        from django.utils import timezone
        return timezone.now() > obj.expires_at
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


@admin.register(TwoFactorLog)
class TwoFactorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'method', 'created_at']
    list_filter = ['action', 'method', 'created_at']
    search_fields = ['user__email', 'action']
    readonly_fields = ['user', 'action', 'method', 'ip_address', 'user_agent', 'error_message', 'created_at']


@admin.register(TwoFactorBackupCode)
class TwoFactorBackupCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_used', 'used_at', 'created_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'code']
    readonly_fields = ['user', 'code', 'is_used', 'used_at', 'created_at']