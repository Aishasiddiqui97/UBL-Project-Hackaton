#!/usr/bin/env python
"""Generate fraud alerts for existing high-risk transactions."""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.transactions.models import Transaction, FraudAlert

def generate_fraud_alerts():
    """Generate fraud alerts for high-risk transactions."""
    print("=" * 70)
    print("🔍 GENERATING FRAUD ALERTS FOR HIGH-RISK TRANSACTIONS")
    print("=" * 70)
    
    # Get high and medium risk transactions
    high_risk_txs = Transaction.objects.filter(
        risk_level__in=['HIGH', 'MEDIUM'],
        fraud_probability__gte=60
    )
    
    print(f"\nFound {high_risk_txs.count()} high-risk transactions")
    
    alerts_created = 0
    alerts_existing = 0
    
    for tx in high_risk_txs:
        # Check if alert already exists
        alert, created = FraudAlert.objects.get_or_create(
            transaction=tx,
            defaults={
                'alert_type': determine_alert_type(tx),
                'probability': tx.fraud_probability,
                'details': generate_alert_details(tx),
                'status': 'OPEN' if tx.risk_level == 'HIGH' else 'IN_PROGRESS'
            }
        )
        
        if created:
            alerts_created += 1
            print(f"\n✅ Created alert for {tx.reference}")
            print(f"   ├─ Type: {alert.alert_type}")
            print(f"   ├─ Probability: {alert.probability:.1f}%")
            print(f"   ├─ Status: {alert.status}")
            print(f"   └─ Amount: PKR {tx.amount:,.2f}")
        else:
            alerts_existing += 1
    
    print("\n" + "=" * 70)
    print(f"✅ Created {alerts_created} new alerts")
    print(f"ℹ️  {alerts_existing} alerts already existed")
    print("=" * 70)
    
    # Summary
    print("\n📊 FRAUD ALERTS SUMMARY:")
    total_alerts = FraudAlert.objects.count()
    print(f"Total Alerts: {total_alerts}")
    print(f"Open: {FraudAlert.objects.filter(status='OPEN').count()}")
    print(f"In Progress: {FraudAlert.objects.filter(status='IN_PROGRESS').count()}")
    print(f"Resolved: {FraudAlert.objects.filter(status='RESOLVED').count()}")
    
    print("\n📋 BY TYPE:")
    print(f"Suspicious Amount: {FraudAlert.objects.filter(alert_type='SUSPICIOUS_AMOUNT').count()}")
    print(f"Unusual Pattern: {FraudAlert.objects.filter(alert_type='UNUSUAL_PATTERN').count()}")
    print(f"Multiple Attempts: {FraudAlert.objects.filter(alert_type='MULTIPLE_ATTEMPTS').count()}")
    print(f"High Risk Location: {FraudAlert.objects.filter(alert_type='HIGH_RISK_LOCATION').count()}")
    
    print("\n🔄 Now refresh your Fraud Detection page!")
    print("📍 URL: http://localhost:3000/fraud-detection")

def determine_alert_type(tx):
    """Determine alert type based on transaction."""
    if tx.amount > 200000:
        return 'SUSPICIOUS_AMOUNT'
    elif tx.amount > 100000:
        return 'UNUSUAL_PATTERN'
    elif tx.fraud_probability > 80:
        return 'HIGH_RISK_LOCATION'
    else:
        return 'MULTIPLE_ATTEMPTS'

def generate_alert_details(tx):
    """Generate alert details."""
    return f"Fraud alert for transaction {tx.reference}: " \
           f"Amount: PKR {tx.amount}, " \
           f"Risk: {tx.risk_level}, " \
           f"Probability: {tx.fraud_probability:.1f}%, " \
           f"Account: {tx.account_number}"

if __name__ == "__main__":
    generate_fraud_alerts()