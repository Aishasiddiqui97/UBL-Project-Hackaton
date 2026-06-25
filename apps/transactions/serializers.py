"""Transaction serializers."""
from rest_framework import serializers
from .models import Transaction, FraudAlert


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'user_email', 'transaction_type', 'amount', 
            'status', 'reference', 'account_number', 'description',
            'risk_level', 'fraud_probability', 'ip_address', 'location',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'reference', 'fraud_probability', 'risk_level', 'created_at', 'updated_at']


class FraudAlertSerializer(serializers.ModelSerializer):
    """Fraud alert serializer."""
    transaction_id = serializers.CharField(source='transaction.reference', read_only=True)
    account_number = serializers.CharField(source='transaction.account_number', read_only=True)
    
    class Meta:
        model = FraudAlert
        fields = [
            'id', 'transaction', 'transaction_id', 'account_number',
            'alert_type', 'status', 'probability', 'details',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionListSerializer(serializers.ModelSerializer):
    """Simplified transaction serializer for list views."""
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'reference', 'account_number', 'transaction_type', 
            'amount', 'status', 'risk_level', 'fraud_probability',
            'created_at'
        ]
