#!/usr/bin/env python
"""Quickly create a new transaction for testing."""
import os
import django
from decimal import Decimal
import uuid

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.transactions.models import Transaction

User = get_user_model()

def create_test_transaction():
    """Create a test transaction."""
    try:
        # Get admin user
        admin_user = User.objects.get(email='admin@example.com')
        
        # Create transaction
        transaction = Transaction.objects.create(
            user=admin_user,
            transaction_type='PAYMENT',
            amount=Decimal('99999.00'),
            reference=f"TXN-{uuid.uuid4().hex[:8].upper()}",
            account_number=f'ACC-NEW-{uuid.uuid4().hex[:6].upper()}',
            description='✨ NEW TEST TRANSACTION - Check frontend now!',
            ip_address='192.168.1.100',
            location='Karachi'
        )
        
        print("=" * 60)
        print("✅ NEW TRANSACTION CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Reference ID: {transaction.reference}")
        print(f"Account: {transaction.account_number}")
        print(f"Amount: PKR {transaction.amount:,.2f}")
        print(f"Type: {transaction.transaction_type}")
        print(f"Status: {transaction.status}")
        print(f"Risk Level: {transaction.risk_level}")
        print(f"Fraud Probability: {transaction.fraud_probability}%")
        print(f"Description: {transaction.description}")
        print("=" * 60)
        print("\n🔄 Now refresh your frontend page to see it!")
        print("📍 URL: http://localhost:3000/transactions")
        print("\nTotal transactions in DB:", Transaction.objects.count())
        
    except User.DoesNotExist:
        print("❌ Admin user not found. Run reset_admin_password.py first")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_test_transaction()