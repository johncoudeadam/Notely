"""
@description
Note models for the Simple Note Taking App.
This module defines the Note model that represents user notes in the system.

Key features:
- User-owned notes with foreign key relationship to CustomUser
- Title and plain text content fields
- Automatic timestamp tracking for creation and updates
- Database optimization with indexes on frequently queried fields

@dependencies
- django.db: Django's database models framework
- django.conf: Django settings for accessing AUTH_USER_MODEL

@notes
- Uses settings.AUTH_USER_MODEL for foreign key to maintain flexibility
- Title is required but content can be empty
- Automatic ordering by creation date (newest first)
- Indexes on user and created_at fields for query performance
"""

from django.conf import settings
from django.db import models


class Note(models.Model):
    """
    Note model representing a user's note in the system.
    
    This model stores plain text notes that belong to specific users.
    Each note has a title, content, and automatic timestamps.
    
    Attributes:
        user (ForeignKey): Reference to the user who owns this note
        title (CharField): Title of the note (required)
        content (TextField): Plain text content of the note
        created_at (DateTimeField): Timestamp when the note was created
        updated_at (DateTimeField): Timestamp when the note was last updated
    """
    
    # Foreign key to the custom user model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        help_text='The user who owns this note.'
    )
    
    # Title field - required
    title = models.CharField(
        max_length=255,
        help_text='Title of the note (required).'
    )
    
    # Content field - plain text, can be empty
    content = models.TextField(
        blank=True,
        help_text='Plain text content of the note.'
    )
    
    # Timestamp fields for tracking record lifecycle
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when the note was created.'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when the note was last updated.'
    )
    
    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-created_at']  # Newest notes first
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['title']),  # For search functionality
        ]
    
    def __str__(self):
        """
        Return string representation of the note.
        
        Returns:
            str: Note title truncated to 50 characters if necessary
        """
        return self.title[:50] + ('...' if len(self.title) > 50 else '')
    
    def get_absolute_url(self):
        """
        Return the canonical URL for this note.
        
        Returns:
            str: URL path to view this note
        """
        from django.urls import reverse
        return reverse('note-detail', kwargs={'pk': self.pk})
