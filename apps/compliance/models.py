"""Compliance models."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ComplianceStatus(models.TextChoices):
    """Compliance status choices."""
    COMPLIANT = 'COMPLIANT', 'Compliant'
    NON_COMPLIANT = 'NON_COMPLIANT', 'Non-Compliant'
    PENDING_REVIEW = 'PENDING_REVIEW', 'Pending Review'
    EXEMPTED = 'EXEMPTED', 'Exempted'
    UNDER_INVESTIGATION = 'UNDER_INVESTIGATION', 'Under Investigation'


class RegulationType(models.TextChoices):
    """Regulation type choices."""
    AML = 'AML', 'Anti-Money Laundering'
    KYC = 'KYC', 'Know Your Customer'
    CTF = 'CTF', 'Counter-Terrorism Financing'
    GDPR = 'GDPR', 'General Data Protection Regulation'
    PCI_DSS = 'PCI_DSS', 'Payment Card Industry DSS'
    SOX = 'SOX', 'Sarbanes-Oxley Act'
    BASEL_III = 'BASEL_III', 'Basel III'
    LOCAL_REGULATION = 'LOCAL_REGULATION', 'Local Regulation'


class ComplianceRule(models.Model):
    """Compliance rule/regulation model."""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    regulation_type = models.CharField(max_length=20, choices=RegulationType.choices)
    
    # Rule details
    severity = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')
    ], default='MEDIUM')
    
    # Applicability
    applies_to_transaction_types = models.JSONField(default=list)
    applies_to_amount_threshold = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    applies_to_countries = models.JSONField(default=list)
    
    # Rule logic (simplified)
    rule_config = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField()
    effective_until = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'compliance_rules'
        ordering = ['-severity', 'code']
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class ComplianceCheck(models.Model):
    """Compliance check result for transactions/entities."""
    # Related entity
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    
    # Check details
    rule = models.ForeignKey(ComplianceRule, on_delete=models.PROTECT, related_name='checks')
    status = models.CharField(max_length=20, choices=ComplianceStatus.choices)
    
    # Results
    passed = models.BooleanField(default=False)
    score = models.FloatField(help_text="Compliance score 0-100")
    findings = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    
    # Metadata
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='compliance_checks')
    checked_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_compliance_checks')
    review_notes = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'compliance_checks'
        ordering = ['-checked_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['status']),
            models.Index(fields=['rule', 'status']),
        ]
    
    def __str__(self) -> str:
        return f"Check {self.id} - {self.rule.code} - {self.status}"


class ComplianceReport(models.Model):
    """Compliance reports for regulatory filing."""
    REPORT_TYPES = [
        ('SAR', 'Suspicious Activity Report'),
        ('CTR', 'Currency Transaction Report'),
        ('STR', 'Suspicious Transaction Report'),
        ('PERIODIC', 'Periodic Compliance Report'),
        ('AD_HOC', 'Ad Hoc Report'),
    ]
    
    report_number = models.CharField(max_length=50, unique=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Draft'),
        ('PENDING_APPROVAL', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('FILED', 'Filed'),
        ('REJECTED', 'Rejected'),
    ], default='DRAFT')
    
    # Content
    data = models.JSONField(default=dict)
    findings_summary = models.TextField(null=True, blank=True)
    
    # Assignment
    prepared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prepared_reports')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_reports')
    
    # Dates
    prepared_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    filed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'compliance_reports'
        ordering = ['-prepared_at']
    
    def __str__(self) -> str:
        return f"{self.report_number} - {self.report_type}"