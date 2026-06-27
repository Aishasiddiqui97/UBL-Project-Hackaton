"""KYC admin."""
from django.contrib import admin
from .models import KYCProfile, KYCDocument, KYCCheck


class KYCDocumentInline(admin.TabularInline):
    model = KYCDocument
    extra = 0
    readonly_fields = ['uploaded_at', 'verified_by', 'verified_at']
    fields = ['document_type', 'file', 'filename', 'is_verified', 'verified_by', 'verified_at']


class KYCCheckInline(admin.TabularInline):
    model = KYCCheck
    extra = 0
    readonly_fields = ['created_at', 'reviewed_by', 'reviewed_at', 'completed_at']
    fields = ['check_type', 'status', 'score', 'provider', 'reviewed_by', 'reviewed_at']


@admin.register(KYCProfile)
class KYCProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'status', 'risk_rating', 'nationality', 'submitted_at', 'approved_at', 'expires_at']
    list_filter = ['status', 'risk_rating', 'nationality', 'country_of_residence', 'submitted_at']
    search_fields = ['user__email', 'user__full_name', 'full_name', 'id_document_number']
    readonly_fields = ['user', 'submitted_at', 'approved_at', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at']
    inlines = [KYCDocumentInline, KYCCheckInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('full_name', 'date_of_birth', 'nationality', 'country_of_residence')
        }),
        ('Contact', {
            'fields': ('phone_number', 'email', 'address', 'city', 'postal_code')
        }),
        ('Identity Document', {
            'fields': ('id_document_type', 'id_document_number', 'id_document_expiry', 'id_document_country')
        }),
        ('Employment/Business', {
            'fields': ('employment_status', 'employer_name', 'occupation', 'annual_income', 'source_of_funds')
        }),
        ('Business Details', {
            'fields': ('business_name', 'business_registration_number', 'business_type', 'business_address')
        }),
        ('KYC Status', {
            'fields': ('status', 'risk_rating', 'reviewed_by', 'reviewed_at', 'review_notes', 'rejection_reason')
        }),
        ('Dates', {
            'fields': ('submitted_at', 'approved_at', 'expires_at')
        }),
        ('Metadata', {
            'fields': ('metadata', 'tags', 'is_active')
        }),
    )


@admin.register(KYCDocument)
class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ['kyc_profile', 'document_type', 'filename', 'is_verified', 'verified_by', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['kyc_profile__user__email', 'filename']
    readonly_fields = ['kyc_profile', 'filename', 'file_size', 'content_type', 'uploaded_at']


@admin.register(KYCCheck)
class KYCCheckAdmin(admin.ModelAdmin):
    list_display = ['kyc_profile', 'check_type', 'status', 'score', 'provider', 'created_at']
    list_filter = ['check_type', 'status', 'provider', 'created_at']
    search_fields = ['kyc_profile__user__email', 'provider_reference']
    readonly_fields = ['created_at', 'completed_at']