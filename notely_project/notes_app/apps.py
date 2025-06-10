"""
@description
Django app configuration for notes_app.
This module defines the configuration for the notes application within
the Simple Note Taking App.

Key features:
- Proper app registration with Django
- Verbose naming for admin interface
- Auto field configuration for model primary keys

@dependencies
- django.apps: Django's application framework

@notes
- Configures the notes_app for Django's app registry
- Sets up default auto field behavior for models
- Provides human-readable name for admin interface
"""

from django.apps import AppConfig


class NotesAppConfig(AppConfig):
    """
    Django app configuration for the notes application.
    
    This configuration class sets up the notes_app with appropriate
    settings for integration with the Django framework.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes_app'
    verbose_name = 'Notes'
