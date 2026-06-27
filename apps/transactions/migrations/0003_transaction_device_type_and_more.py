"""
Transaction migration to add new fraud detection fields.

This migration adds the following fields to the Transaction model:
- device_type: Device type used for the transaction (Mobile, Desktop, ATM, POS)
- is_new_location: Boolean indicating if the transaction location is new/unfamiliar
- risk_score: Integer field for the calculated risk score (0-100)
- risk_level: Char field storing the risk level (LOW, MEDIUM, HIGH)
- fraud_probability: Float field for the fraud probability percentage

These fields are used by the fraud detection and risk scoring systems.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='device_type',
            field=models.CharField(choices=[('MOBILE', 'Mobile'), ('DESKTOP', 'Desktop'), ('ATM', 'ATM'), ('POS', 'POS')], default='MOBILE', max_length=20, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='fraud_probability',
            field=models.FloatField(default=0.0, help_text='Fraud probability percentage (0-100)'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_new_location',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='risk_score',
            field=models.IntegerField(default=0, help_text='Aggregated risk score (0-100)'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='risk_level',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='LOW', max_length=10, null=True),
            preserve_default=False,
        ),
    ]