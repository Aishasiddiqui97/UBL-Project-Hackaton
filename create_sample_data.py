#!/usr/bin/env python
"""Create sample transaction and fraud data for testing."""
import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.transactions.models import Transaction, FraudAlert

User = get_user_model()

def create_sample_data():
    """Create sample transactions and fraud alerts."""
    print("🔄 Creating sample data...")
    
    # Get or create admin user
    try:
        admin_user = User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            username='admin',
            full_name='Admin User'
        )
    
    # Create sample users
    users = []
    for i in range(5):
        user, created = User.objects.get_or_create(
            email=f'user{i+1}@example.com',
            defaults={
                'username': f'user{i+1}',
                'full_name': f'Test User {i+1}',
                'role': 'USER'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)
    
    # Add admin to users list
    users.append(admin_user)
    
    # Clear existing transactions
    Transaction.objects.all().delete()
    FraudAlert.objects.all().delete()
    
    # Transaction types and amounts
    tx_types = ['DEBIT', 'CREDIT', 'TRANSFER', 'PAYMENT']
    amounts = [5000, 15000, 25000, 50000, 75000, 100000, 150000, 200000, 500000, 1000000]
    locations = ['Karachi', 'Lahore', 'Islamabad', 'Faisalabad', 'Rawalpindi']
    
    # Create 50 sample transactions
    transactions = []
    for i in range(50):
        user = random.choice(users)
        amount = Decimal(str(random.choice(amounts)))
        tx_type = random.choice(tx_types)
        
        # Generate unique reference
        import uuid
        reference = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # Create transaction
        transaction = Transaction.objects.create(
            user=user,
            transaction_type=tx_type,
            amount=amount,
            reference=reference,
            account_number=f'ACC-{10000000 + i}',
            description=f'Sample {tx_type.lower()} transaction #{i+1}',
            ip_address=f'192.168.1.{random.randint(1, 255)}',
            location=random.choice(locations),
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        
        transactions.append(transaction)
        
        # Create fraud alert for high-risk transactions
        if transaction.risk_level == 'HIGH' and transaction.fraud_probability > 70:
            alert_types = ['SUSPICIOUS_AMOUNT', 'UNUSUAL_PATTERN', 'HIGH_RISK_LOCATION']
            
            FraudAlert.objects.create(
                transaction=transaction,
                alert_type=random.choice(alert_types),
                probability=transaction.fraud_probability,
                details=f'Alert for transaction {transaction.reference}: High fraud probability detected',
                status=random.choice(['OPEN', 'IN_PROGRESS'])
            )
    
    print(f"✅ Created {Transaction.objects.count()} transactions")
    print(f"✅ Created {FraudAlert.objects.count()} fraud alerts")
    
    # Print some statistics
    stats = {
        'total': Transaction.objects.count(),
        'flagged': Transaction.objects.filter(status='FLAGGED').count(),
        'under_review': Transaction.objects.filter(status='UNDER_REVIEW').count(),
        'clear': Transaction.objects.filter(status='CLEAR').count(),
        'high_risk': Transaction.objects.filter(risk_level='HIGH').count(),
        'medium_risk': Transaction.objects.filter(risk_level='MEDIUM').count(),
        'low_risk': Transaction.objects.filter(risk_level='LOW').count(),
    }
    
    print("\n📊 Statistics:")
    print(f"Total transactions: {stats['total']}")
    print(f"Status breakdown:")
    print(f"  - Flagged: {stats['flagged']}")
    print(f"  - Under Review: {stats['under_review']}")
    print(f"  - Clear: {stats['clear']}")
    print(f"Risk breakdown:")
    print(f"  - High Risk: {stats['high_risk']}")
    print(f"  - Medium Risk: {stats['medium_risk']}")
    print(f"  - Low Risk: {stats['low_risk']}")
    
    print("\n🎉 Sample data created successfully!")
    print("\nYou can now test:")
    print("- Transaction Monitoring: http://localhost:3000/transactions")
    print("- Fraud Detection: http://localhost:3000/fraud-detection")

if __name__ == "__main__":
    create_sample_data()