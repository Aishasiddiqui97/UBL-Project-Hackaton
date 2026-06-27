"""Compliance admin."""
from django.contrib import admin
from .models import ComplianceRule, ComplianceCheck, ComplianceReport


@admin.register(ComplianceRule)
class ComplianceRuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'regulation_type', 'severity', 'is_active', 'effective_from']
    list_filter = ['regulation_type', 'severity', 'is_active', 'effective_from']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'regulation_type', 'severity')
        }),
        ('Applicability', {
            'fields': ('applies_to_transaction_types', 'applies_to_amount_threshold', 'applies_to_countries')
        }),
        ('Rule Logic', {
            'fields': ('rule_config',)
        }),
        ('Validity', {
            'fields': ('is_active', 'effective_from', 'effective_until')
        }),
    )


@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'rule', 'transaction_id', 'user_id', 'status', 'passed', 'score', 'checked_at']
    list_filter = ['status', 'rule__regulation_type', 'passed', 'checked_at']
    search_fields = ['transaction_id', 'user_id', 'account_number', 'rule__code']
    readonly_fields = ['checked_by', 'checked_at']
    date_hierarchy = 'checked_at'


@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ['report_number', 'report_type', 'title', 'status', 'period_start', 'period_end', 'prepared_by', 'prepared_at']
    list_filter = ['report_type', 'status', 'prepared_at']
    search_fields = ['report_number', 'title', 'description']
    readonly_fields = ['report_number', 'prepared_by', 'prepared_at', 'approved_at', 'filed_at']
    date_hierarchy = 'prepared_at'