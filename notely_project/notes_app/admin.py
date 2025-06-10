"""
@description
Django admin configuration for the notes_app.
This module configures the Django admin interface for Note model management.

Key features:
- Custom admin interface for Note model
- List display showing key note information
- Filtering and searching capabilities for administrators
- Read-only fields for automatic timestamps

@dependencies
- django.contrib.admin: Django's admin framework
- .models: Local Note model

@notes
- Provides efficient note management for administrators
- Includes user information in list display for oversight
- Search functionality for finding notes by title and content
- Filters help administrators navigate large numbers of notes
"""

from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the Note model.
    
    This admin class provides a comprehensive interface for administrators
    to manage user notes, including viewing, editing, and organizing notes.
    """
    
    # Fields to display in the admin list view
    list_display = [
        'title',
        'user',
        'created_at',
        'updated_at',
        'content_preview',
    ]
    
    # Fields that can be used for filtering
    list_filter = [
        'created_at',
        'updated_at',
        'user',
    ]
    
    # Fields that can be searched
    search_fields = [
        'title',
        'content',
        'user__email',
    ]
    
    # Fields that are read-only (automatic timestamps)
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    # Order records by creation date (newest first)
    ordering = ['-created_at']
    
    # Number of records per page
    list_per_page = 25
    
    # Fields to show when viewing/editing a note
    fields = [
        'user',
        'title',
        'content',
        'created_at',
        'updated_at',
    ]
    
    def content_preview(self, obj):
        """
        Return a preview of the note content for the list display.
        
        Args:
            obj (Note): The note instance
            
        Returns:
            str: Truncated content preview
        """
        if obj.content:
            return obj.content[:100] + ('...' if len(obj.content) > 100 else '')
        return '(No content)'
    
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        """
        Optimize the queryset to reduce database queries.
        
        Args:
            request: HTTP request object
            
        Returns:
            QuerySet: Optimized queryset with related user data
        """
        return super().get_queryset(request).select_related('user')
