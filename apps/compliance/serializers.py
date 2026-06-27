"""Compliance serializers."""
from rest_framework import serializers
from .models import ComplianceRule, ComplianceCheck, ComplianceReport, ComplianceStatus, RegulationType


class ComplianceRuleSerializer(serializers.ModelSerializer):
    """Compliance rule serializer."""
    regulation_type_display = serializers.CharField(source='get_regulation_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = ComplianceRule
        fields = [
            'id', 'code', 'name', 'description', 'regulation_type',
            'regulation_type_display', 'severity', 'severity_display',
            'applies_to_transaction_types', 'applies_to_amount_threshold',
            'applies_to_countries', 'rule_config',
            'is_active', 'effective_from', 'effective_until',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ComplianceCheckSerializer(serializers.ModelSerializer):
    """Compliance check serializer."""
    rule_code = serializers.CharField(source='rule.code', read_only=True)
    rule_name = serializers.CharField(source='rule.name', read_only=True)
    regulation_type = serializers.CharField(source='rule.regulation_type', read_only=True)
    checked_by_email = serializers.CharField(source='checked_by.email', read_only=True)
    reviewed_by_email = serializers.CharField(source='reviewed_by.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ComplianceCheck
        fields = [
            'id', 'transaction_id', 'user_id', 'account_number',
            'rule', 'rule_code', 'rule_name', 'regulation_type',
            'status', 'status_display', 'passed', 'score',
            'findings', 'recommendations',
            'checked_by', 'checked_by_email', 'checked_at',
            'reviewed_at', 'reviewed_by', 'reviewed_by_email', 'review_notes'
        ]
        read_only_fields = ['id', 'checked_at']


class ComplianceReportSerializer(serializers.ModelSerializer):
    """Compliance report serializer."""
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prepared_by_email = serializers.CharField(source='prepared_by.email', read_only=True)
    approved_by_email = serializers.CharField(source='approved_by.email', read_only=True)
    
    class Meta:
        model = ComplianceReport
        fields = [
            'id', 'report_number', 'report_type', 'report_type_display',
            'title', 'description', 'period_start', 'period_end',
            'status', 'status_display', 'data', 'findings_summary',
            'prepared_by', 'prepared_by_email', 'approved_by', 'approved_by_email',
            'prepared_at', 'approved_at', 'filed_at'
        ]
        read_only_fields = ['id', 'report_number', 'prepared_at', 'prepared_by']


class ComplianceCheckCreateSerializer(serializers.ModelSerializer):
    """Compliance check creation serializer."""
    
    class Meta:
        model = ComplianceCheck
        fields = [
            'transaction_id', 'user_id', 'account_number',
            'rule', 'status', 'passed', 'score',
            'findings', 'recommendations'
        ]
    
    def create(self, validated_data):
        validated_data['checked_by'] = self.context['request'].user
        return super().create(validated_data)