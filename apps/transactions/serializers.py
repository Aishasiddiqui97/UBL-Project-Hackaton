"""Transaction serializers."""
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'user_email', 'transaction_type', 'amount', 
                  'status', 'reference', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'reference', 'created_at', 'updated_at']
