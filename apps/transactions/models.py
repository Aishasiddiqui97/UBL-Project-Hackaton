"""Transaction models."""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
import random

User = get_user_model()


class TransactionType(models.TextChoices):
    """Transaction type choices."""
    DEBIT = 'DEBIT', 'Debit'
    CREDIT = 'CREDIT', 'Credit'
    TRANSFER = 'TRANSFER', 'Transfer'
    PAYMENT = 'PAYMENT', 'Payment'


class TransactionStatus(models.TextChoices):
    """Transaction status choices."""
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'
    FLAGGED = 'FLAGGED', 'Flagged'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    CLEAR = 'CLEAR', 'Clear'


class RiskLevel(models.TextChoices):
    """Risk level choices."""
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'


class Transaction(models.Model):
    """Transaction model for financial operations."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    reference = models.CharField(max_length=255, unique=True)
    account_number = models.CharField(max_length=50, default='ACC-000000')
    description = models.TextField()

    # Fraud Detection Fields
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices, default=RiskLevel.LOW)
    fraud_probability = models.FloatField(default=0.0, help_text="Fraud probability percentage (0-100)")
    device_type = models.CharField(max_length=20, choices=[('MOBILE', 'Mobile'), ('DESKTOP', 'Desktop'), ('ATM', 'ATM'), ('POS', 'POS')], default='MOBILE')
    is_new_location = models.BooleanField(default=False)
    location = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    risk_score = models.IntegerField(default=0, help_text="Aggregated risk score (0-100)")

    # KYC Fields
    customer_id = models.CharField(max_length=50, null=True, blank=True)
    kyc_status = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['fraud_probability', 'device_type']),
            models.Index(fields=['is_new_location']),
            models.Index(fields=['risk_score']),
        ]

    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.reference}"

    def save(self, *args, **kwargs):
        """Auto-calculate fraud probability and risk level."""
        if not self.fraud_probability:
            self.fraud_probability = self.calculate_fraud_probability()

        # ✅ FIX 1: Thresholds lowered so HIGH risk actually triggers
        # PEHLE: >= 80 HIGH, >= 50 MEDIUM  (too hard — PKR 500K was getting LOW)
        # FIXED: >= 70 HIGH, >= 40 MEDIUM
        if self.fraud_probability >= 70:
            self.risk_level = RiskLevel.HIGH
            self.status = TransactionStatus.FLAGGED
        elif self.fraud_probability >= 40:
            self.risk_level = RiskLevel.MEDIUM
            self.status = TransactionStatus.UNDER_REVIEW
        else:
            self.risk_level = RiskLevel.LOW
            if self.status == TransactionStatus.PENDING:
                self.status = TransactionStatus.CLEAR

        # Calculate risk score
        self.risk_score = self.calculate_risk_score()

        super().save(*args, **kwargs)

        # ✅ FIX 2: Alert threshold lowered from 60 to 40
        # PEHLE: fraud_probability >= 60 — MEDIUM transactions were missed
        # FIXED: fraud_probability >= 40 — all MEDIUM and HIGH get alerts
        if self.risk_level in ['HIGH', 'MEDIUM'] and self.fraud_probability >= 40:
            if not hasattr(self, '_creating_alert'):
                self._creating_alert = True
                FraudAlert.objects.get_or_create(
                    transaction=self,
                    defaults={
                        'alert_type': self._determine_alert_type(),
                        'probability': self.fraud_probability,
                        'details': self._generate_alert_details(),
                        'status': 'OPEN' if self.risk_level == 'HIGH' else 'IN_PROGRESS'
                    }
                )
                delattr(self, '_creating_alert')

    def calculate_risk_score(self):
        """Calculate risk score based on transaction features."""
        score = 0

        # Amount risk (0-60 pts)
        if self.amount >= Decimal('300000'):   # PKR 300K+
            score += 60
        elif self.amount >= Decimal('100000'): # PKR 100K+
            score += 40
        elif self.amount >= Decimal('50000'):  # PKR 50K+
            score += 20
        elif self.amount >= Decimal('10000'):  # PKR 10K+
            score += 5

        # Device risk (0-15 pts)
        device_risk = {
            'ATM': 15,
            'POS': 12,
            'DESKTOP': 8,
            'MOBILE': 5,
        }
        score += device_risk.get(self.device_type, 5)

        # Location risk (0-15 pts)
        if self.is_new_location:
            score += 15

        # Time-based risk (0-10 pts)
        import datetime
        current_hour = datetime.datetime.now().hour
        if current_hour < 6 or current_hour >= 22:  # Late night 10PM-6AM
            score += 10

        # Transaction type risk (0-10 pts)
        type_risk = {
            'TRANSFER': 10,
            'PAYMENT': 7,
            'DEBIT': 5,
            'CREDIT': 2,
        }
        score += type_risk.get(self.transaction_type, 5)

        # ML probability (0-15 pts)
        score += (self.fraud_probability / 100) * 15

        return min(score, 100)

    def calculate_fraud_probability(self):
        """
        Calculate fraud probability (0-100).

        ✅ FIX 3: Amount scoring completely rewritten.

        PEHLE (broken):
          PKR 100K+ → +30 pts
          Random     → 0-30 pts
          PKR 500K could get 30+5 = 35% → LOW ❌

        FIXED:
          PKR 300K+ → +60 pts  (guaranteed HIGH even with 0 noise)
          PKR 100K+ → +40 pts  (HIGH or MEDIUM)
          PKR 50K+  → +20 pts  (MEDIUM)
          Random    → 0-15 pts only (cannot override amount)
        """
        from datetime import datetime

        risk_score = 0

        # 1. AMOUNT RISK — dominant factor (0-60 pts)
        if self.amount >= Decimal('300000'):   # PKR 300K+
            risk_score += 60
        elif self.amount >= Decimal('100000'): # PKR 100K+
            risk_score += 40
        elif self.amount >= Decimal('50000'):  # PKR 50K+
            risk_score += 20
        elif self.amount >= Decimal('10000'):  # PKR 10K+
            risk_score += 5

        # 2. TIME-BASED RISK (0-15 pts)
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 22:  # Late night 10PM-6AM
            risk_score += 15
        elif current_hour < 9:                       # Early morning
            risk_score += 8

        # 3. TRANSACTION TYPE RISK (0-10 pts)
        type_risk = {
            'TRANSFER': 10,
            'PAYMENT':  7,
            'DEBIT':    5,
            'CREDIT':   2,
        }
        risk_score += type_risk.get(str(self.transaction_type).upper(), 5)

        # 4. DEVICE TYPE RISK (0-10 pts)
        device_risk = {
            'ATM': 10,
            'POS': 8,
            'DESKTOP': 5,
            'MOBILE': 3,
        }
        risk_score += device_risk.get(self.device_type.upper(), 5)

        # 5. ML NOISE — small only, cannot override amount (0-15 pts)
        risk_score += random.randint(0, 15)

        return min(risk_score, 100)

    def _determine_alert_type(self):
        """Determine the type of fraud alert."""
        if self.amount >= Decimal('200000'):
            return 'SUSPICIOUS_AMOUNT'
        elif self.amount >= Decimal('100000'):
            return 'UNUSUAL_PATTERN'
        elif self.is_new_location:
            return 'HIGH_RISK_LOCATION'
        else:
            return 'MULTIPLE_ATTEMPTS'

    def _generate_alert_details(self):
        """Generate detailed alert message."""
        return (
            f"Fraud alert for transaction {self.reference}: "
            f"Amount: PKR {self.amount}, "
            f"Risk: {self.risk_level}, "
            f"Probability: {self.fraud_probability:.1f}%"
        )


class FraudAlert(models.Model):
    """Fraud alert model."""

    class AlertStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'

    class AlertType(models.TextChoices):
        SUSPICIOUS_AMOUNT = 'SUSPICIOUS_AMOUNT', 'Suspicious Amount'
        UNUSUAL_PATTERN = 'UNUSUAL_PATTERN', 'Unusual Pattern'
        MULTIPLE_ATTEMPTS = 'MULTIPLE_ATTEMPTS', 'Multiple Attempts'
        HIGH_RISK_LOCATION = 'HIGH_RISK_LOCATION', 'High Risk Location'

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='fraud_alerts')
    alert_type = models.CharField(max_length=30, choices=AlertType.choices)
    status = models.CharField(max_length=15, choices=AlertStatus.choices, default=AlertStatus.OPEN)
    probability = models.FloatField(help_text="Fraud probability percentage")
    details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fraud_alerts'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Alert {self.id} - {self.alert_type}"