"""KYC models."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class KYCStatus(models.TextChoices):
    """KYC status choices."""
    NOT_STARTED = 'NOT_STARTED', 'Not Started'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    PENDING_REVIEW = 'PENDING_REVIEW', 'Pending Review'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    EXPIRED = 'EXPIRED', 'Expired'
    REQUIRES_UPDATE = 'REQUIRES_UPDATE', 'Requires Update'


class DocumentType(models.TextChoices):
    """Document type choices."""
    NATIONAL_ID = 'NATIONAL_ID', 'National ID'
    PASSPORT = 'PASSPORT', 'Passport'
    DRIVING_LICENSE = 'DRIVING_LICENSE', 'Driving License'
    PROOF_OF_ADDRESS = 'PROOF_OF_ADDRESS', 'Proof of Address'
    BANK_STATEMENT = 'BANK_STATEMENT', 'Bank Statement'
    UTILITY_BILL = 'UTILITY_BILL', 'Utility Bill'
    TAX_CERTIFICATE = 'TAX_CERTIFICATE', 'Tax Certificate'
    BUSINESS_REGISTRATION = 'BUSINESS_REGISTRATION', 'Business Registration'
    SELFIE = 'SELFIE', 'Selfie/Photo'
    OTHER = 'OTHER', 'Other'


class RiskRating(models.TextChoices):
    """Customer risk rating."""
    LOW = 'LOW', 'Low Risk'
    MEDIUM = 'MEDIUM', 'Medium Risk'
    HIGH = 'HIGH', 'High Risk'
    PROHIBITED = 'PROHIBITED', 'Prohibited'


class KYCProfile(models.Model):
    """KYC Profile for customers."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc_profile')
    
    # Personal Information
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    country_of_residence = models.CharField(max_length=100, null=True, blank=True)
    
    # Contact
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Identity Documents
    id_document_type = models.CharField(max_length=30, choices=DocumentType.choices, null=True, blank=True)
    id_document_number = models.CharField(max_length=100, null=True, blank=True)
    id_document_expiry = models.DateField(null=True, blank=True)
    id_document_country = models.CharField(max_length=100, null=True, blank=True)
    
    # Employment/Business
    employment_status = models.CharField(max_length=50, null=True, blank=True)
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    source_of_funds = models.TextField(null=True, blank=True)
    
    # Business (if applicable)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    business_registration_number = models.CharField(max_length=100, null=True, blank=True)
    business_type = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    
    # KYC Status
    status = models.CharField(max_length=20, choices=KYCStatus.choices, default=KYCStatus.NOT_STARTED)
    risk_rating = models.CharField(max_length=20, choices=RiskRating.choices, default=RiskRating.LOW)
    
    # Review
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_kyc_profiles')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    
    # Dates
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'kyc_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['risk_rating']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self) -> str:
        return f"KYC - {self.user.email} - {self.status}"


class KYCDocument(models.Model):
    """KYC Document uploads."""
    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    file = models.FileField(upload_to='kyc_documents/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    content_type = models.CharField(max_length=100)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verified_kyc_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(null=True, blank=True)
    
    # OCR/Extracted Data
    extracted_data = models.JSONField(default=dict, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'kyc_documents'
        ordering = ['-uploaded_at']
    
    def __str__(self) -> str:
        return f"{self.document_type} - {self.kyc_profile.user.email}"


class KYCCheck(models.Model):
    """KYC verification checks."""
    CHECK_TYPES = [
        ('IDENTITY', 'Identity Verification'),
        ('ADDRESS', 'Address Verification'),
        ('PEP', 'PEP/Sanctions Screening'),
        ('ADVERSE_MEDIA', 'Adverse Media Check'),
        ('DOCUMENT', 'Document Verification'),
        ('BIOMETRIC', 'Biometric Verification'),
    ]
    
    CHECK_STATUS = [
        ('PENDING', 'Pending'),
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
        ('MANUAL_REVIEW', 'Manual Review Required'),
    ]
    
    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='checks')
    check_type = models.CharField(max_length=20, choices=CHECK_TYPES)
    status = models.CharField(max_length=20, choices=CHECK_STATUS, default='PENDING')
    
    # Results
    score = models.FloatField(null=True, blank=True, help_text="Check score 0-100")
    details = models.JSONField(default=dict, blank=True)
    provider = models.CharField(max_length=100, null=True, blank=True)
    provider_reference = models.CharField(max_length=255, null=True, blank=True)
    
    # Review
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_kyc_checks')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'kyc_checks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['kyc_profile', 'check_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self) -> str:
        return f"{self.check_type} - {self.kyc_profile.user.email} - {self.status}"