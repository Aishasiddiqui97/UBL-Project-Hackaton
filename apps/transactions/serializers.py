"""Transaction serializers."""
from rest_framework import serializers
from .models import Transaction, FraudAlert


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    fraud_reason = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'user_email', 'transaction_type', 'amount', 
            'status', 'reference', 'account_number', 'description',
            'risk_level', 'fraud_probability', 'ip_address', 'location',
            'created_at', 'updated_at', 'fraud_reason'
        ]
        read_only_fields = ['id', 'user', 'reference', 'fraud_probability', 'risk_level', 'created_at', 'updated_at']

    def get_fraud_reason(self, obj):
        """Get the latest fraud alert reason for this transaction."""
        latest_alert = obj.fraud_alerts.first()
        if latest_alert:
            return {
                'alert_type': latest_alert.alert_type,
                'details': latest_alert.details,
                'probability': latest_alert.probability
            }
        return None


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
    fraud_reason = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'reference', 'account_number', 'transaction_type', 
            'amount', 'status', 'risk_level', 'fraud_probability',
            'created_at', 'fraud_reason'
        ]

    def get_fraud_reason(self, obj):
        """Get the latest fraud alert reason for this transaction."""
        latest_alert = obj.fraud_alerts.first()
        if latest_alert:
            return {
                'alert_type': latest_alert.alert_type,
                'details': latest_alert.details,
                'probability': latest_alert.probability
            }
        return None
