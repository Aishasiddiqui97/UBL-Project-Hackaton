"""Cases models."""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class CaseStatus(models.TextChoices):
    """Case status choices."""
    OPEN = 'OPEN', 'Open'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    ESCALATED = 'ESCALATED', 'Escalated'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'
    REJECTED = 'REJECTED', 'Rejected'


class CasePriority(models.TextChoices):
    """Case priority choices."""
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'


class CaseType(models.TextChoices):
    """Case type choices."""
    FRAUD_INVESTIGATION = 'FRAUD_INVESTIGATION', 'Fraud Investigation'
    KYC_REVIEW = 'KYC_REVIEW', 'KYC Review'
    COMPLIANCE_CHECK = 'COMPLIANCE_CHECK', 'Compliance Check'
    SUSPICIOUS_ACTIVITY = 'SUSPICIOUS_ACTIVITY', 'Suspicious Activity'
    REGULATORY_REPORTING = 'REGULATORY_REPORTING', 'Regulatory Reporting'
    CUSTOMER_COMPLAINT = 'CUSTOMER_COMPLAINT', 'Customer Complaint'
    INTERNAL_AUDIT = 'INTERNAL_AUDIT', 'Internal Audit'


class Case(models.Model):
    """Case management model."""
    case_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Classification
    case_type = models.CharField(max_length=30, choices=CaseType.choices)
    status = models.CharField(max_length=20, choices=CaseStatus.choices, default=CaseStatus.OPEN)
    priority = models.CharField(max_length=10, choices=CasePriority.choices, default=CasePriority.MEDIUM)
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_cases'
    )
    
    # Related entities
    related_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    related_user_id = models.CharField(max_length=100, null=True, blank=True)
    related_account_number = models.CharField(max_length=50, null=True, blank=True)
    
    # Dates
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolution = models.TextField(null=True, blank=True)
    resolution_summary = models.TextField(null=True, blank=True)
    
    # Metadata
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cases'
        ordering = ['-opened_at']
        indexes = [
            models.Index(fields=['case_number']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['case_type']),
            models.Index(fields=['opened_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.case_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.status in [CaseStatus.RESOLVED, CaseStatus.CLOSED] and not self.closed_at:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)


class CaseComment(models.Model):
    """Case comments/notes."""
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_comments')
    content = models.TextField()
    is_internal = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'case_comments'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"Comment on {self.case.case_number} by {self.author.email}"


class CaseDocument(models.Model):
    """Case documents/attachments."""
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_documents')
    file = models.FileField(upload_to='case_documents/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    content_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'case_documents'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.filename} - {self.case.case_number}"