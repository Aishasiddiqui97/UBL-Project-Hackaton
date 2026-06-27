"""Fraud detection operations."""
import json
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model
from apps.fraud_detection.predict import predict_transaction
from apps.fraud_detection.train_model import train_model
from .models import Transaction, FraudAlert
from apps.notifications.services import NotificationService

User = get_user_model()


def detect_fraud_for_transaction(transaction_id, force_recalculate=False):
    """Run ML model to detect fraud for a transaction.
    
    Args:
        transaction_id: ID of the transaction to analyze
        force_recalculate: If True, force re-calculation even if recent results exist
    
    Returns:
        dict: Analysis results including fraud probability, prediction, and risk scores
    """
    try:
        transaction = Transaction.objects.select_related('user').get(id=transaction_id)
    except Transaction.DoesNotExist:
        return {'success': False, 'message': 'Transaction not found'}
    
    # Check cache for recent results
    cache_key = f'fraud_analysis_{transaction_id}'
    cached_result = cache.get(cache_key)
    
    if cached_result and not force_recalculate:
        # Check if cache is recent (within last 10 minutes)
        cached_time = cached_result.get('timestamp')
        if cached_time and timezone.now() < cached_time + timezone.timedelta(minutes=10):
            return cached_result
    
    # Get user data for ML model
    user = transaction.user
    
    # Build input for ML model
    input_data = {
        'account_no': user.account_number if hasattr(user, 'account_number') else str(user.id),
        'amount': float(transaction.amount),
        'location': transaction.location or 'Unknown',
        'transaction_count': 0,  # This would need to be calculated based on user history
        'transaction_type': transaction.transaction_type,
        'device_type': 'Unknown',  # This would need to be added as a field
        'is_new_location': False,  # This would need to be calculated
    }
    
    # Run fraud detection
    try:
        prediction_result = predict_transaction(input_data)
    except Exception as e:
        # If prediction fails, calculate based on transaction amount and type
        fraud_probability = calculate_rule_based_fraud_probability(transaction)
        risk_score = calculate_risk_score(
            amount=transaction.amount,
            transaction_count=0,
            is_new_location=False,
            fraud_probability=fraud_probability
        )
        prediction_result = {
            'fraud_probability': fraud_probability,
            'prediction': 'Fraud' if fraud_probability > 50 else 'Normal'
        }
    
    # Extract results
    fraud_probability = prediction_result.get('fraud_probability', 0)
    prediction = prediction_result.get('prediction', 'Normal')
    
    # Calculate risk scores
    risk_score = calculate_risk_score(
        amount=transaction.amount,
        transaction_count=0,
        is_new_location=False,
        fraud_probability=fraud_probability
    )
    
    # Determine transaction risk level
    risk_level = transaction.risk_level
    if fraud_probability >= 70:
        risk_level = 'HIGH'
    elif fraud_probability >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    # Update transaction
    transaction.fraud_probability = fraud_probability
    transaction.risk_level = risk_level
    transaction.save()
    
    # Create fraud alert if needed
    if fraud_probability >= 40 and transaction.status in ['PENDING', 'FLAGGED']:
        create_fraud_alert(transaction, fraud_probability, prediction)
    
    # Prepare result
    result = {
        'success': True,
        'transaction_id': transaction_id,
        'fraud_probability': fraud_probability,
        'prediction': prediction,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'needs_attention': fraud_probability >= 40,
        'timestamp': timezone.now()
    }
    
    # Cache the result
    cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
    
    # Send notification if fraud detected
    if fraud_probability >= 70:
        NotificationService.send_system_alert(
            f'High fraud probability detected for transaction {transaction.reference}',
            {'type': 'FRAUD_HIGH', 'transaction_id': transaction_id}
        )
    
    return result


def calculate_rule_based_fraud_probability(transaction):
    """Calculate fraud probability using rule-based logic when ML model is unavailable."""
    probability = 0
    
    # High amount risk
    if transaction.amount >= 100000:
        probability += 30
    elif transaction.amount >= 50000:
        probability += 20
    elif transaction.amount >= 10000:
        probability += 10
    
    # Risk based on transaction type
    high_risk_types = ['TRANSFER', 'PAYMENT']
    if transaction.transaction_type in high_risk_types:
        probability += 15
    
    # Time-based risk
    current_hour = timezone.now().hour
    if current_hour < 6 or current_hour >= 22:
        probability += 10
    
    # Large transaction counts
    transaction_count = Transaction.objects.filter(
        user=transaction.user,
        created_at__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    if transaction_count > 50:
        probability += 25
    
    return min(probability, 100)


def calculate_risk_score(amount, transaction_count, is_new_location, fraud_probability):
    """Calculate risk score based on transaction features."""
    score = 0
    
    # Amount risk
    if amount >= 100000:
        score += 60
    elif amount >= 50000:
        score += 40
    elif amount >= 10000:
        score += 20
    
    # Transaction count risk
    if transaction_count > 50:
        score += 30
    elif transaction_count > 20:
        score += 15
    
    # New location risk
    if is_new_location:
        score += 25
    
    # Fraud probability risk
    score += (fraud_probability * 0.5)
    
    # Time-based risk
    current_hour = timezone.now().hour
    if current_hour < 6 or current_hour >= 22:
        score += 15
    
    return min(score, 100)


def create_fraud_alert(transaction, probability, prediction):
    """Create a fraud alert for a transaction."""
    try:
        alert, created = FraudAlert.objects.get_or_create(
            transaction=transaction,
            defaults={
                'alert_type': 'HIGH_RISK_TRANSACTION',
                'probability': probability,
                'details': f"Fraud prediction: {prediction}, Probability: {probability}%",
                'status': 'OPEN' if probability >= 70 else 'IN_PROGRESS'
            }
        )
        
        # Update transaction status based on probability
        if probability >= 70:
            transaction.status = 'FLAGGED'
        elif probability >= 40:
            transaction.status = 'UNDER_REVIEW'
        
        transaction.save()
        
        return alert
    except Exception:
        return None


def analyze_transaction_network(transaction_id):
    """Analyze transaction network relationships for fraud detection."""
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        user = transaction.user
    except Transaction.DoesNotExist:
        return {'success': False, 'message': 'Transaction not found'}
    
    # Get user's transactions
    user_transactions = Transaction.objects.filter(
        user=user
    ).select_related('user').order_by('-created_at')
    
    # Calculate network metrics
    metrics = {
        'total_transactions': user_transactions.count(),
        'high_risk_transactions': user_transactions.filter(risk_level='HIGH').count(),
        'recent_transactions': user_transactions.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).count(),
        'average_amount': user_transactions.aggregate(
            avg=models.Avg('amount')
        ).get('avg__avg') or 0,
        'max_amount': user_transactions.aggregate(
            max=models.Max('amount')
        ).get('max__max') or 0,
    }
    
    # Calculate velocity (transactions per day)
    if metrics['total_transactions'] > 0:
        days_active = max(1, (timezone.now() - user_transactions.first().created_at).days)
        metrics['transaction_velocity'] = metrics['total_transactions'] / days_active
    else:
        metrics['transaction_velocity'] = 0
    
    # Detect pattern anomalies
    anomalies = []
    if metrics['recent_transactions'] > 50:
        anomalies.append({
            'type': 'HIGH_ACTIVITY',
            'severity': 'HIGH',
            'description': f"High transaction velocity: {metrics['transaction_velocity']:.2f} transactions/day"
        })
    
    if metrics['max_amount'] > 100000:
        anomalies.append({
            'type': 'LARGE_TRANSACTION',
            'severity': 'MEDIUM',
            'description': f"Large transaction detected: ${metrics['max_amount']:,.2f}"
        })
    
    # Pattern-based fraud indicators
    if metrics['total_transactions'] > 10 and metrics['average_amount'] < 1000:
        anomalies.append({
            'type': 'MICRO_TRANSACTIONS',
            'severity': 'MEDIUM',
            'description': "Multiple small transactions detected"
        })
    
    # Risk score based on network analysis
    network_risk_score = min(100, (
        (metrics['high_risk_transactions'] / max(1, metrics['total_transactions']) * 50) +
        (min(metrics['transaction_velocity'], 10) * 3) +
        (metrics['max_amount'] / 10000)
    ))
    
    return {
        'success': True,
        'transaction_id': transaction_id,
        'metrics': metrics,
        'anomalies': anomalies,
        'network_risk_score': network_risk_score,
        'requires_review': len(anomalies) > 0,
        'generated_at': timezone.now()
    }


def get_fraud_alerts_stats():
    """Get fraud detection statistics for monitoring."""
    from django.db.models import Count, Avg, Q
    
    # Overall stats
    total_transactions = Transaction.objects.count()
    high_risk_transactions = Transaction.objects.filter(risk_level='HIGH').count()
    medium_risk_transactions = Transaction.objects.filter(risk_level='MEDIUM').count()
    
    # Fraud probability stats
    fraud_stats = Transaction.objects.aggregate(
        avg_fraud_probability=Avg('fraud_probability'),
        max_fraud_probability=Avg('fraud_probability', filter=Q(fraud_probability__gt=50)),
    )
    
    # Alert stats
    total_alerts = FraudAlert.objects.count()
    open_alerts = FraudAlert.objects.filter(status='OPEN').count()
    resolved_alerts = FraudAlert.objects.filter(status='RESOLVED').count()
    
    # Time-based analysis
    from django.db.models import F
    transactions_24h = Transaction.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).count()
    
    return {
        'total_transactions': total_transactions,
        'high_risk_count': high_risk_transactions,
        'medium_risk_count': medium_risk_transactions,
        'high_risk_percentage': round((high_risk_transactions / max(1, total_transactions)) * 100, 2),
        'average_fraud_probability': round(fraud_stats['avg_fraud_probability'] or 0, 2),
        'high_fraud_probability_count': round(fraud_stats['max_fraud_probability'] or 0),
        'total_alerts': total_alerts,
        'open_alerts': open_alerts,
        'resolved_alerts': resolved_alerts,
        'transactions_last_24h': transactions_24h,
        'updated_at': timezone.now()
    }


def batch_fraud_analysis(transaction_ids):
    """Run fraud analysis on a batch of transactions."""
    results = []
    failed = []
    
    for transaction_id in transaction_ids:
        try:
            result = detect_fraud_for_transaction(transaction_id)
            if result['success']:
                results.append(result)
            else:
                failed.append({
                    'transaction_id': transaction_id,
                    'error': result['message']
                })
        except Exception as e:
            failed.append({
                'transaction_id': transaction_id,
                'error': str(e)
            })
    
    return {
        'success': True,
        'processed': len(results),
        'failed': len(failed),
        'results': results,
        'failed_transactions': failed,
        'processed_at': timezone.now()
    }


def cleanup_old_fraud_data(days=30):
    """Clean up old fraud detection data to manage storage."""
    from django.utils import timezone as tz
    
    # Delete old fraud alerts
    old_alerts = FraudAlert.objects.filter(
        created_at__lt=tz.now() - timezone.timedelta(days=days),
        status__in=['RESOLVED', 'CLOSED']
    )
    alert_count = old_alerts.count()
    old_alerts.delete()
    
    # Clear cache for old transactions
    old_cache_keys = [f'fraud_analysis_{id}' for id in 
                     Transaction.objects.filter(
                         created_at__lt=tz.now() - timezone.timedelta(days=days)
                     ).values_list('id', flat=True)]
    
    # Note: Cache clearing should be done at application level
    
    return {
        'success': True,
        'alerts_deleted': alert_count,
        'cleaned_up_at': tz.now()
    }