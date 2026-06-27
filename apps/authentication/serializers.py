"""Two-factor authentication serializers."""
from rest_framework import serializers
from .models import TwoFactorSetup, TwoFactorToken, TwoFactorBackupCode, TwoFactorMethod


class TwoFactorSetupSerializer(serializers.ModelSerializer):
    """Two-factor authentication setup serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    primary_method_display = serializers.CharField(source='get_primary_method_display', read_only=True)
    
    class Meta:
        model = TwoFactorSetup
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'primary_method', 'primary_method_display',
            'backup_methods', 'is_enabled', 'is_required',
            'email_verified', 'email', 'phone_number', 'phone_verified',
            'secret_key', 'recovery_codes', 'hardware_key_id',
            'last_used_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TwoFactorTokenSerializer(serializers.ModelSerializer):
    """Two-factor authentication token serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = TwoFactorToken
        fields = [
            'id', 'user', 'user_email', 'token', 'method', 'method_display',
            'ip_address', 'user_agent', 'device', 'created_at', 'expires_at',
            'used_at', 'is_used', 'is_expired'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return timezone.now() > obj.expires_at


class TwoFactorBackupCodeSerializer(serializers.ModelSerializer):
    """Two-factor authentication backup code serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = TwoFactorBackupCode
        fields = [
            'id', 'user', 'user_email', 'code', 'is_used', 'used_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TwoFactorSetupUpdateSerializer(serializers.ModelSerializer):
    """Two-factor authentication setup update serializer."""
    
    class Meta:
        model = TwoFactorSetup
        fields = [
            'primary_method', 'backup_methods', 'is_enabled', 'is_required',
            'email', 'phone_number', 'secret_key', 'recovery_codes',
            'hardware_key_id'
        ]


class TwoFactorVerifySerializer(serializers.Serializer):
    """Two-factor authentication verification serializer."""
    token = serializers.CharField(required=False, allow_null=True)
    code = serializers.CharField(required=False, allow_null=True)
    method = serializers.ChoiceField(choices=TwoFactorMethod.choices)
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    recovery_code = serializers.CharField(required=False, allow_null=True)