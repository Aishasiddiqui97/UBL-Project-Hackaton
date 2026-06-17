"""Payment admin."""
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment admin."""
    list_display = ['transaction_id', 'user', 'order', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['transaction_id', 'user__email']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']
