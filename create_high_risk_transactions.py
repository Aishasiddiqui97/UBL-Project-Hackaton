#!/usr/bin/env python
"""Create high-risk transactions with fraud alerts."""
import os
import django
from decimal import Decimal
import uuid
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.transactions.models import Transaction, FraudAlert

User = get_user_model()

def create_high_risk_transactions():
    """Create multiple high-risk transactions to trigger fraud alerts."""
    try:
        admin_user = User.objects.get(email='admin@example.com')
        
        # High-risk scenarios
        scenarios = [
            {
                'name': '🚨 VERY HIGH RISK - Large Late Night Transfer',
                'type': 'TRANSFER',
                'amount': Decimal('850000.00'),
                'description': 'Large transfer at unusual hour - HIGH FRAUD RISK'
            },
            {
                'name': '🚨 HIGH RISK - Suspicious Payment Pattern',
                'type': 'PAYMENT',
                'amount': Decimal('450000.00'),
                'description': 'Unusual payment pattern detected - Multiple large amounts'
            },
            {
                'name': '⚠️ MEDIUM-HIGH RISK - Multiple Attempts',
                'type': 'DEBIT',
                'amount': Decimal('320000.00'),
                'description': 'Multiple transaction attempts from same account'
            },
            {
                'name': '🚨 HIGH RISK - Foreign Transaction',
                'type': 'TRANSFER',
                'amount': Decimal('750000.00'),
                'description': 'Large international transfer - High risk location'
            },
            {
                'name': '⚠️ MEDIUM RISK - Unusual Pattern',
                'type': 'PAYMENT',
                'amount': Decimal('280000.00'),
                'description': 'Transaction pattern deviation detected'
            },
            {
                'name': '🚨 CRITICAL - Money Laundering Risk',
                'type': 'TRANSFER',
                'amount': Decimal('950000.00'),
                'description': 'Potential money laundering - Immediate review required'
            },
            {
                'name': '⚠️ HIGH AMOUNT - Round Number',
                'type': 'PAYMENT',
                'amount': Decimal('500000.00'),
                'description': 'Large round number payment - Suspicious pattern'
            },
            {
                'name': '🚨 FLAGGED - Velocity Check Failed',
                'type': 'DEBIT',
                'amount': Decimal('650000.00'),
                'description': 'Transaction velocity exceeded normal threshold'
            },
        ]
        
        print("=" * 70)
        print("🚨 CREATING HIGH-RISK TRANSACTIONS WITH FRAUD ALERTS")
        print("=" * 70)
        
        created_transactions = []
        created_alerts = []
        
        for scenario in scenarios:
            # Create transaction
            tx = Transaction.objects.create(
                user=admin_user,
                transaction_type=scenario['type'],
                amount=scenario['amount'],
                reference=f"TXN-{uuid.uuid4().hex[:8].upper()}",
                account_number=f'ACC-FRAUD-{uuid.uuid4().hex[:4].upper()}',
                description=scenario['description'],
                ip_address=f'192.168.{random.randint(1,255)}.{random.randint(1,255)}',
                location=random.choice(['Karachi', 'Lahore', 'Dubai', 'London', 'Unknown'])
            )
            
            created_transactions.append(tx)
            
            # Manually increase fraud probability for high-risk ones
            if scenario['amount'] > 500000:
                tx.fraud_probability = min(random.randint(70, 95), 100)
                if tx.fraud_probability >= 80:
                    tx.risk_level = 'HIGH'
                    tx.status = 'FLAGGED'
                elif tx.fraud_probability >= 60:
                    tx.risk_level = 'MEDIUM'
                    tx.status = 'UNDER_REVIEW'
                tx.save()
            
            # Create fraud alert
            if tx.fraud_probability >= 60:
                alert = FraudAlert.objects.create(
                    transaction=tx,
                    alert_type=determine_alert_type(tx),
                    probability=tx.fraud_probability,
                    details=generate_alert_details(tx, scenario['name']),
                    status='OPEN' if tx.fraud_probability >= 80 else 'IN_PROGRESS'
                )
                created_alerts.append(alert)
            
            print(f"\n{scenario['name']}")
            print(f"  ├─ Reference: {tx.reference}")
            print(f"  ├─ Amount: PKR {tx.amount:,.2f}")
            print(f"  ├─ Status: {tx.status}")
            print(f"  ├─ Risk: {tx.risk_level}")
            print(f"  ├─ Fraud %: {tx.fraud_probability:.1f}%")
            if tx.fraud_probability >= 60:
                print(f"  └─ 🚨 ALERT CREATED")
        
        print("\n" + "=" * 70)
        print(f"✅ Created {len(created_transactions)} high-risk transactions")
        print(f"🚨 Created {len(created_alerts)} fraud alerts")
        print("=" * 70)
        
        # Final summary
        print("\n📊 COMPLETE FRAUD DETECTION SUMMARY:")
        print(f"\n🔢 TRANSACTIONS:")
        print(f"  Total: {Transaction.objects.count()}")
        print(f"  Flagged: {Transaction.objects.filter(status='FLAGGED').count()}")
        print(f"  Under Review: {Transaction.objects.filter(status='UNDER_REVIEW').count()}")
        print(f"  Clear: {Transaction.objects.filter(status='CLEAR').count()}")
        
        print(f"\n🚨 FRAUD ALERTS:")
        print(f"  Total: {FraudAlert.objects.count()}")
        print(f"  Open: {FraudAlert.objects.filter(status='OPEN').count()}")
        print(f"  In Progress: {FraudAlert.objects.filter(status='IN_PROGRESS').count()}")
        print(f"  Resolved: {FraudAlert.objects.filter(status='RESOLVED').count()}")
        
        print("\n🔄 REFRESH YOUR FRAUD DETECTION PAGE!")
        print("📍 URL: http://localhost:3000/fraud-detection")
        print("\n💡 You should now see:")
        print("  ✓ Multiple fraud alerts in the list")
        print("  ✓ Updated statistics at the top")
        print("  ✓ Suspicious transactions table")
        print("  ✓ Alert details when clicked")
        
    except User.DoesNotExist:
        print("❌ Admin user not found")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def determine_alert_type(tx):
    """Determine alert type."""
    if tx.amount > 700000:
        return 'HIGH_RISK_LOCATION'
    elif tx.amount > 400000:
        return 'SUSPICIOUS_AMOUNT'
    elif tx.amount > 250000:
        return 'UNUSUAL_PATTERN'
    else:
        return 'MULTIPLE_ATTEMPTS'

def generate_alert_details(tx, scenario_name):
    """Generate detailed alert message."""
    return f"{scenario_name}\n" \
           f"Transaction: {tx.reference}\n" \
           f"Amount: PKR {tx.amount:,}\n" \
           f"Account: {tx.account_number}\n" \
           f"Location: {tx.location}\n" \
           f"Fraud Probability: {tx.fraud_probability:.1f}%"

if __name__ == "__main__":
    create_high_risk_transactions()