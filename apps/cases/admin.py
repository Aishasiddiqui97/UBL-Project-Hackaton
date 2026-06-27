"""Cases admin."""
from django.contrib import admin
from .models import Case, CaseComment, CaseDocument


class CaseCommentInline(admin.TabularInline):
    model = CaseComment
    extra = 0
    readonly_fields = ['author', 'created_at', 'updated_at']
    fields = ['author', 'content', 'is_internal', 'created_at']


class CaseDocumentInline(admin.TabularInline):
    model = CaseDocument
    extra = 0
    readonly_fields = ['uploaded_by', 'filename', 'file_size', 'created_at']
    fields = ['uploaded_by', 'file', 'filename', 'description', 'created_at']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'title', 'case_type', 'status', 'priority', 'assigned_to', 'opened_at', 'due_date']
    list_filter = ['case_type', 'status', 'priority', 'opened_at', 'assigned_to']
    search_fields = ['case_number', 'title', 'description', 'related_transaction_id']
    readonly_fields = ['case_number', 'opened_at', 'closed_at', 'created_by', 'updated_at']
    inlines = [CaseCommentInline, CaseDocumentInline]
    date_hierarchy = 'opened_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('case_number', 'title', 'description', 'case_type', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Related Entities', {
            'fields': ('related_transaction_id', 'related_user_id', 'related_account_number')
        }),
        ('Dates', {
            'fields': ('opened_at', 'closed_at', 'due_date')
        }),
        ('Resolution', {
            'fields': ('resolution', 'resolution_summary')
        }),
        ('Metadata', {
            'fields': ('tags', 'metadata', 'is_active')
        }),
    )


@admin.register(CaseComment)
class CaseCommentAdmin(admin.ModelAdmin):
    list_display = ['case', 'author', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['case__case_number', 'author__email', 'content']
    readonly_fields = ['author', 'created_at', 'updated_at']


@admin.register(CaseDocument)
class CaseDocumentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'case', 'uploaded_by', 'file_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['case__case_number', 'filename', 'uploaded_by__email']
    readonly_fields = ['uploaded_by', 'filename', 'file_size', 'content_type', 'created_at']