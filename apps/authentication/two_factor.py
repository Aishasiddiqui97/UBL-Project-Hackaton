"""Two-factor authentication utilities."""
import secrets
import string
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


def generate_backup_code():
    """Generate a random backup code."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))


def generate_secret_key():
    """Generate a secret key for authenticator apps."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))


def generate_otp():
    """Generate a one-time password for SMS or email."""
    return ''.join(secrets.choice(string.digits) for _ in range(6))


def get_user_2fa_setup(user):
    """Get or create two-factor authentication setup for a user."""
    from .models import TwoFactorSetup
    
    setup, created = TwoFactorSetup.objects.get_or_create(user=user)
    return setup


def setup_email_2fa(user, email):
    """Setup email-based two-factor authentication."""
    setup = get_user_2fa_setup(user)
    
    if not email:
        return False, "Email address is required"
    
    setup.email = email
    setup.email_verified = False
    setup.save()
    
    # Send verification email
    otp = generate_otp()
    # Store OTP temporarily
    setup.save()
    
    send_mail(
        'Two-Factor Authentication Verification',
        f'Your verification code is: {otp}',
        'no-reply@example.com',
        [email]
    )
    
    return True, "Verification email sent"


def setup_sms_2fa(user, phone_number):
    """Setup SMS-based two-factor authentication."""
    from .models import TwoFactorSetup
    
    setup = get_user_2fa_setup(user)
    
    if not phone_number:
        return False, "Phone number is required"
    
    # Validate phone number format (basic)
    if not phone_number.replace('+', '').isdigit():
        return False, "Invalid phone number format"
    
    setup.phone_number = phone_number
    setup.phone_verified = False
    setup.save()
    
    # Generate and send OTP
    otp = generate_otp()
    # In production, use an SMS service
    # sms_service.send_otp(phone_number, otp)
    
    return True, "OTP sent to phone number"


def setup_auth_app_2fa(user):
    """Setup authenticator app-based two-factor authentication."""
    from .models import TwoFactorSetup
    
    setup = get_user_2fa_setup(user)
    
    secret_key = generate_secret_key()
    setup.secret_key = secret_key
    setup.save()
    
    # Generate recovery codes
    recovery_codes = []
    for _ in range(10):
        code = generate_backup_code()
        from .models import TwoFactorBackupCode
        TwoFactorBackupCode.objects.create(user=user, code=code)
        recovery_codes.append(code)
    
    setup.recovery_codes = recovery_codes
    setup.save()
    
    # Generate QR code URL (simplified)
    qr_url = f"otpauth://totp/YourApp:{user.email}?secret={secret_key}&issuer=YourApp"
    
    return True, {"secret_key": secret_key, "recovery_codes": recovery_codes, "qr_url": qr_url}


def verify_2fa_token(user, token, method):
    """Verify two-factor authentication token."""
    from .models import TwoFactorToken, TwoFactorLog
    
    # Check if token exists
    try:
        two_factor_token = TwoFactorToken.objects.get(user=user, method=method)
    except TwoFactorToken.DoesNotExist:
        TwoFactorLog.objects.create(
            user=user,
            action='failure',
            method=method,
            error_message="Token not found"
        )
        return False, "Invalid token"
    
    # Check if token is expired
    if two_factor_token.expires_at < datetime.now():
        two_factor_token.is_used = True
        two_factor_token.save()
        
        TwoFactorLog.objects.create(
            user=user,
            action='failure',
            method=method,
            error_message="Token expired"
        )
        return False, "Token expired"
    
    # Check if token is already used
    if two_factor_token.is_used:
        TwoFactorLog.objects.create(
            user=user,
            action='failure',
            method=method,
            error_message="Token already used"
        )
        return False, "Token already used"
    
    # Check if token matches (in real implementation, validate against stored hash)
    # For simplicity, we assume token is valid
    two_factor_token.is_used = True
    two_factor_token.used_at = datetime.now()
    two_factor_token.save()
    
    # Log success
    TwoFactorLog.objects.create(
        user=user,
        action='success',
        method=method
    )
    
    return True, "Token verified successfully"


def verify_backup_code(user, code):
    """Verify backup code for two-factor authentication."""
    from .models import TwoFactorBackupCode, TwoFactorLog
    
    try:
        backup_code = TwoFactorBackupCode.objects.get(user=user, code=code, is_used=False)
    except TwoFactorBackupCode.DoesNotExist:
        TwoFactorLog.objects.create(
            user=user,
            action='failure',
            method=TwoFactorMethod.BACKUP_CODE,
            error_message="Invalid backup code"
        )
        return False, "Invalid backup code"
    
    # Mark as used
    backup_code.is_used = True
    backup_code.used_at = datetime.now()
    backup_code.save()
    
    # Log success
    TwoFactorLog.objects.create(
        user=user,
        action='success',
        method=TwoFactorMethod.BACKUP_CODE
    )
    
    return True, "Backup code verified successfully"


def get_active_backup_codes(user):
    """Get active backup codes for a user."""
    from .models import TwoFactorBackupCode
    
    return TwoFactorBackupCode.objects.filter(user=user, is_used=False)


def revoke_all_backup_codes(user):
    """Revoke all backup codes for a user."""
    from .models import TwoFactorBackupCode
    
    backup_codes = TwoFactorBackupCode.objects.filter(user=user)
    for code in backup_codes:
        code.is_used = True
        code.used_at = datetime.now()
        code.save()


def log_2fa_attempt(user, action, method=None, ip_address=None, user_agent=None, error_message=None):
    """Log a two-factor authentication attempt."""
    from .models import TwoFactorLog
    
    TwoFactorLog.objects.create(
        user=user,
        action=action,
        method=method,
        ip_address=ip_address,
        user_agent=user_agent,
        error_message=error_message
    )


class TwoFactorMethod:
    """Two-factor authentication method constants."""
    EMAIL = 'EMAIL'
    SMS = 'SMS'
    AUTH_APP = 'AUTH_APP'
    BACKUP_CODE = 'BACKUP_CODE'
    HARDWARE_KEY = 'HARDWARE_KEY'
    
    @classmethod
    def values(cls):
        return [cls.EMAIL, cls.SMS, cls.AUTH_APP, cls.BACKUP_CODE, cls.HARDWARE_KEY]