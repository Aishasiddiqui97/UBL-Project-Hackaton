"""KYC serializers."""
from rest_framework import serializers
from .models import KYCProfile, KYCDocument, KYCCheck, KYCStatus, DocumentType, RiskRating


class KYCDocumentSerializer(serializers.ModelSerializer):
    """KYC document serializer."""
    verified_by_email = serializers.CharField(source='verified_by.email', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = KYCDocument
        fields = [
            'id', 'kyc_profile', 'document_type', 'document_type_display',
            'file', 'filename', 'file_size', 'content_type',
            'is_verified', 'verified_by', 'verified_by_email',
            'verified_at', 'verification_notes', 'extracted_data',
            'uploaded_at'
        ]
        read_only_fields = ['id', 'file_size', 'uploaded_at']


class KYCCheckSerializer(serializers.ModelSerializer):
    """KYC check serializer."""
    check_type_display = serializers.CharField(source='get_check_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewed_by_email = serializers.CharField(source='reviewed_by.email', read_only=True)
    
    class Meta:
        model = KYCCheck
        fields = [
            'id', 'kyc_profile', 'check_type', 'check_type_display',
            'status', 'status_display', 'score', 'details',
            'provider', 'provider_reference',
            'reviewed_by', 'reviewed_by_email', 'reviewed_at', 'review_notes',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at']


class KYCProfileSerializer(serializers.ModelSerializer):
    """KYC profile serializer."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    reviewed_by_email = serializers.CharField(source='reviewed_by.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    risk_rating_display = serializers.CharField(source='get_risk_rating_display', read_only=True)
    id_document_type_display = serializers.CharField(source='get_id_document_type_display', read_only=True)
    documents = KYCDocumentSerializer(many=True, read_only=True)
    checks = KYCCheckSerializer(many=True, read_only=True)
    document_count = serializers.SerializerMethodField()
    pending_checks = serializers.SerializerMethodField()
    
    class Meta:
        model = KYCProfile
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'full_name', 'date_of_birth', 'nationality', 'country_of_residence',
            'phone_number', 'email', 'address', 'city', 'postal_code',
            'id_document_type', 'id_document_type_display', 'id_document_number',
            'id_document_expiry', 'id_document_country',
            'employment_status', 'employer_name', 'occupation', 'annual_income',
            'source_of_funds',
            'business_name', 'business_registration_number', 'business_type', 'business_address',
            'status', 'status_display', 'risk_rating', 'risk_rating_display',
            'reviewed_by', 'reviewed_by_email', 'reviewed_at', 'review_notes', 'rejection_reason',
            'submitted_at', 'approved_at', 'expires_at',
            'metadata', 'tags',
            'is_active', 'created_at', 'updated_at',
            'documents', 'checks', 'document_count', 'pending_checks'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def get_document_count(self, obj):
        return obj.documents.count()
    
    def get_pending_checks(self, obj):
        return obj.checks.filter(status='PENDING').count()


class KYCProfileListSerializer(serializers.ModelSerializer):
    """Simplified KYC profile serializer for list views."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    risk_rating_display = serializers.CharField(source='get_risk_rating_display', read_only=True)
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = KYCProfile
        fields = [
            'id', 'user_email', 'full_name', 'status', 'status_display',
            'risk_rating', 'risk_rating_display', 'submitted_at', 'approved_at',
            'expires_at', 'document_count', 'created_at'
        ]
    
    def get_document_count(self, obj):
        return obj.documents.count()


class KYCProfileCreateSerializer(serializers.ModelSerializer):
    """KYC profile creation serializer."""
    
    class Meta:
        model = KYCProfile
        fields = [
            'full_name', 'date_of_birth', 'nationality', 'country_of_residence',
            'phone_number', 'email', 'address', 'city', 'postal_code',
            'id_document_type', 'id_document_number', 'id_document_expiry', 'id_document_country',
            'employment_status', 'employer_name', 'occupation', 'annual_income',
            'source_of_funds',
            'business_name', 'business_registration_number', 'business_type', 'business_address',
            'metadata', 'tags'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = KYCStatus.IN_PROGRESS
        validated_data['submitted_at'] = timezone.now()
        return super().create(validated_data)


class KYCDocumentUploadSerializer(serializers.ModelSerializer):
    """KYC document upload serializer."""
    
    class Meta:
        model = KYCDocument
        fields = ['document_type', 'file']
    
    def create(self, validated_data):
        kyc_profile_id = self.context.get('kyc_profile_id')
        file = validated_data['file']
        validated_data['kyc_profile_id'] = kyc_profile_id
        validated_data['filename'] = file.name
        validated_data['file_size'] = file.size
        validated_data['content_type'] = file.content_type
        return super().create(validated_data)


class KYCReviewSerializer(serializers.Serializer):
    """KYC review serializer."""
    status = serializers.ChoiceField(choices=[KYCStatus.APPROVED, KYCStatus.REJECTED, KYCStatus.REQUIRES_UPDATE])
    review_notes = serializers.CharField(required=False, allow_blank=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    risk_rating = serializers.ChoiceField(choices=RiskRating.choices, required=False)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)