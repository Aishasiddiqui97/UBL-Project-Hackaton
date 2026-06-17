"""Payment serializers."""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'user', 'user_email', 'amount', 
                  'status', 'method', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'transaction_id', 'created_at', 'updated_at']
