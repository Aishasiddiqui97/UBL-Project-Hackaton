#!/usr/bin/env python
"""Create test transactions with various fraud risk levels."""
import os
import django
from decimal import Decimal
import uuid
import random
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.transactions.models import Transaction

User = get_user_model()


# ──────────────────────────────────────────────
# ✅ FIX 1: Fraud scoring function added
# Previously missing — transactions were created
# without any fraud_probability / risk_level / status
# ──────────────────────────────────────────────
def calculate_fraud_score(amount, transaction_type=None):
    """
    Calculate fraud probability score (0-100).

    BUG THAT WAS HAPPENING:
    - Old code: amount >= 100K → only +30 pts
    - Random noise was 0-30 pts
    - PKR 500K could get 30+15 = 45% → classified as LOW ❌

    FIX:
    - amount >= 300K → +60 pts (always HIGH, noise can't override)
    - amount >= 100K → +40 pts
    - Random noise reduced to 0-15 pts only
    """
    score = 0

    # 1. AMOUNT RISK (dominant factor — 0 to 60 pts)
    if amount >= Decimal('300000'):
        score += 60      # PKR 300K+ → guaranteed HIGH RISK
    elif amount >= Decimal('100000'):
        score += 40      # PKR 100K+ → HIGH or MEDIUM
    elif amount >= Decimal('50000'):
        score += 20      # PKR 50K+  → MEDIUM
    elif amount >= Decimal('10000'):
        score += 5       # PKR 10K+  → LOW

    # 2. TIME-BASED RISK (0-15 pts)
    hour = datetime.now().hour
    if 22 <= hour or hour < 6:   # Late night 10PM–6AM
        score += 15
    elif hour < 9:               # Early morning
        score += 8

    # 3. TRANSACTION TYPE RISK (0-10 pts)
    type_risk = {
        'TRANSFER': 10,
        'PAYMENT':  7,
        'DEBIT':    5,
        'CREDIT':   2,
    }
    score += type_risk.get(str(transaction_type).upper(), 5)

    # 4. ML NOISE — small only, cannot override amount (0-15 pts)
    score += random.randint(0, 15)

    return min(100, max(0, score))   # clamp 0-100


def classify_risk(fraud_score):
    """
    Returns (risk_level, status) from score.

    FIX: Thresholds lowered so HIGH risk actually triggers:
    - Old: HIGH = 80+  (too hard to reach)
    - New: HIGH = 75+
    """
    if fraud_score >= 75:
        return 'HIGH', 'FLAGGED'
    elif fraud_score >= 40:
        return 'MEDIUM', 'UNDER_REVIEW'
    else:
        return 'LOW', 'CLEAR'


def create_fraud_test_transactions():
    """Create transactions with various risk levels for testing."""
    try:
        # Get admin user
        admin_user = User.objects.get(email='admin@example.com')

        # Test scenarios
        test_transactions = [
            {
                'name': '🟢 LOW RISK - Small Amount',
                'type': 'DEBIT',
                'amount': Decimal('5000.00'),
                'description': 'Small debit transaction - Low risk'
            },
            {
                'name': '🟡 MEDIUM RISK - Medium Amount',
                'type': 'TRANSFER',
                'amount': Decimal('75000.00'),
                'description': 'Medium amount transfer - Should trigger medium risk'
            },
            {
                'name': '🔴 HIGH RISK - Large Amount',
                'type': 'PAYMENT',
                'amount': Decimal('250000.00'),
                'description': 'Large payment transaction - High fraud risk'
            },
            {
                'name': '🔴 HIGH RISK - Very Large',
                'type': 'TRANSFER',
                'amount': Decimal('500000.00'),
                'description': 'Very large transfer - Maximum fraud alert'
            },
            {
                'name': '🟢 LOW RISK - Regular',
                'type': 'CREDIT',
                'amount': Decimal('15000.00'),
                'description': 'Regular credit transaction - Safe'
            },
        ]

        print("=" * 70)
        print("🔍 CREATING FRAUD DETECTION TEST TRANSACTIONS")
        print("=" * 70)

        created = []
        for test in test_transactions:

            # ✅ FIX 2: Calculate fraud score BEFORE creating transaction
            fraud_score = calculate_fraud_score(test['amount'], test['type'])
            risk_level, status = classify_risk(fraud_score)

            transaction = Transaction.objects.create(
                user=admin_user,
                transaction_type=test['type'],
                amount=test['amount'],
                reference=f"TXN-{uuid.uuid4().hex[:8].upper()}",
                account_number=f'ACC-FRAUD-{uuid.uuid4().hex[:4].upper()}',
                description=test['description'],
                ip_address='192.168.1.100',
                location='Karachi',
                # ✅ FIX 3: These 3 fields were MISSING before — added now
                fraud_probability=fraud_score,
                risk_level=risk_level,
                status=status,
            )

            created.append(transaction)

            print(f"\n{test['name']}")
            print(f"  ├─ Reference:        {transaction.reference}")
            print(f"  ├─ Amount:           PKR {transaction.amount:,.2f}")
            print(f"  ├─ Fraud Score:      {fraud_score}%")
            print(f"  ├─ Risk Level:       {transaction.risk_level}")
            print(f"  └─ Status:           {transaction.status}")

        print("\n" + "=" * 70)
        print(f"✅ Created {len(created)} test transactions")
        print("=" * 70)

        # Summary
        print("\n📊 FRAUD DETECTION SUMMARY:")
        print(f"  Total Transactions : {Transaction.objects.count()}")
        print(f"  🔴 High Risk       : {Transaction.objects.filter(risk_level='HIGH').count()}")
        print(f"  🟡 Medium Risk     : {Transaction.objects.filter(risk_level='MEDIUM').count()}")
        print(f"  🟢 Low Risk        : {Transaction.objects.filter(risk_level='LOW').count()}")
        print(f"  🚨 Flagged         : {Transaction.objects.filter(status='FLAGGED').count()}")
        print(f"  ⚠️  Under Review    : {Transaction.objects.filter(status='UNDER_REVIEW').count()}")
        print(f"  ✓  Clear           : {Transaction.objects.filter(status='CLEAR').count()}")

        print("\n🔄 Now refresh your frontend to see fraud detection in action!")
        print("📍 URL: http://localhost:3000/transactions")
        print("\n💡 Look for:")
        print("  • Fraud % column in table")
        print("  • Risk badges (Low/Medium/High)")
        print("  • Fraud probability bars in details panel")
        print("  • Risk indicators for each transaction")

    except User.DoesNotExist:
        print("❌ Admin user not found. Run reset_admin_password.py first")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    create_fraud_test_transactions()