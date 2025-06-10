"""
@description
Configuration file for the users Django application.
This module defines the UsersConfig class that configures the users app
within the Django project.

@dependencies
- django.apps: Django application configuration framework

@notes
- Sets default_auto_field to BigAutoField for better performance with large datasets
- Defines the app name as 'users' for Django's app registry
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the users Django application.
    
    This class configures the users app and defines its metadata
    for Django's application registry.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users' 