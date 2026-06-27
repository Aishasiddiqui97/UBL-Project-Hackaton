"""Cases serializers."""
from rest_framework import serializers
from .models import Case, CaseComment, CaseDocument, CaseStatus, CasePriority, CaseType


class CaseDocumentSerializer(serializers.ModelSerializer):
    """Case document serializer."""
    uploaded_by_email = serializers.CharField(source='uploaded_by.email', read_only=True)
    
    class Meta:
        model = CaseDocument
        fields = [
            'id', 'case', 'uploaded_by', 'uploaded_by_email',
            'file', 'filename', 'file_size', 'content_type',
            'description', 'created_at'
        ]
        read_only_fields = ['id', 'file_size', 'created_at']


class CaseCommentSerializer(serializers.ModelSerializer):
    """Case comment serializer."""
    author_email = serializers.CharField(source='author.email', read_only=True)
    author_full_name = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = CaseComment
        fields = [
            'id', 'case', 'author', 'author_email', 'author_full_name',
            'content', 'is_internal', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class CaseSerializer(serializers.ModelSerializer):
    """Case serializer."""
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)
    assigned_to_full_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    case_type_display = serializers.CharField(source='get_case_type_display', read_only=True)
    comments = CaseCommentSerializer(many=True, read_only=True)
    documents = CaseDocumentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        fields = [
            'id', 'case_number', 'title', 'description',
            'case_type', 'case_type_display', 'status', 'status_display',
            'priority', 'priority_display',
            'assigned_to', 'assigned_to_email', 'assigned_to_full_name',
            'created_by', 'created_by_email',
            'related_transaction_id', 'related_user_id', 'related_account_number',
            'opened_at', 'closed_at', 'due_date',
            'resolution', 'resolution_summary',
            'tags', 'metadata',
            'is_active', 'updated_at',
            'comments', 'documents', 'comment_count', 'document_count'
        ]
        read_only_fields = ['id', 'case_number', 'opened_at', 'closed_at', 'created_by', 'updated_at']
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class CaseListSerializer(serializers.ModelSerializer):
    """Simplified case serializer for list views."""
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    case_type_display = serializers.CharField(source='get_case_type_display', read_only=True)
    comment_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        fields = [
            'id', 'case_number', 'title', 'case_type', 'case_type_display',
            'status', 'status_display', 'priority', 'priority_display',
            'assigned_to_email', 'opened_at', 'due_date',
            'comment_count', 'document_count'
        ]
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class CaseCreateSerializer(serializers.ModelSerializer):
    """Case creation serializer."""
    
    class Meta:
        model = Case
        fields = [
            'title', 'description', 'case_type', 'priority',
            'assigned_to', 'related_transaction_id', 'related_user_id',
            'related_account_number', 'due_date', 'tags', 'metadata'
        ]
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['case_number'] = self.generate_case_number()
        return super().create(validated_data)
    
    def generate_case_number(self):
        from django.utils import timezone
        import uuid
        date_str = timezone.now().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:6].upper()
        return f"CASE-{date_str}-{unique_id}"