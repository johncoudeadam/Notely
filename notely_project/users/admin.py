"""
@description
Django admin configuration for the users app.
This module configures the Django admin interface for the CustomUser model,
providing administrators with a user-friendly interface for user management.

Key features:
- Custom admin interface for user management
- Display of key user fields in list view
- Filtering and searching capabilities
- Fieldset organization for better UX

@dependencies
- django.contrib: Django's admin framework
- .models: Local CustomUser model

@notes
- Extends UserAdmin to maintain Django's built-in user management features
- Customizes fieldsets to include role and timestamp fields
- Provides filtering by role and active status for easy user management
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.
    
    This class extends Django's built-in UserAdmin to provide
    a customized admin interface that includes the additional
    fields specific to our CustomUser model.
    
    Features:
    - Display email, role, and status in list view
    - Filter by role and active status
    - Search by email and first/last name
    - Organized fieldsets for better admin UX
    """
    
    # Fields to display in the admin list view
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'role', 
        'is_active', 
        'created_at',
        'last_login'
    )
    
    # Fields that can be used to filter the list view
    list_filter = (
        'role', 
        'is_active', 
        'is_staff', 
        'is_superuser',
        'created_at',
        'last_login'
    )
    
    # Fields that can be searched
    search_fields = ('email', 'first_name', 'last_name')
    
    # Default ordering for the list view
    ordering = ('-created_at',)
    
    # Fields that are read-only in the admin interface
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    # Custom fieldsets for the user edit form
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name'),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff'),
        }),
    )
    
    # Actions available in the admin list view
    actions = ['activate_users', 'deactivate_users', 'make_admin', 'make_regular']
    
    def activate_users(self, request, queryset):
        """
        Admin action to activate selected users.
        
        Args:
            request: HTTP request object
            queryset: Selected user objects
        """
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} user(s) were successfully activated.'
        )
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """
        Admin action to deactivate selected users.
        
        Args:
            request: HTTP request object
            queryset: Selected user objects
        """
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} user(s) were successfully deactivated.'
        )
    deactivate_users.short_description = "Deactivate selected users"
    
    def make_admin(self, request, queryset):
        """
        Admin action to promote selected users to administrator role.
        
        Args:
            request: HTTP request object
            queryset: Selected user objects
        """
        updated = queryset.update(role=CustomUser.ADMIN)
        self.message_user(
            request,
            f'{updated} user(s) were promoted to administrator.'
        )
    make_admin.short_description = "Promote to administrator"
    
    def make_regular(self, request, queryset):
        """
        Admin action to demote selected users to regular user role.
        
        Args:
            request: HTTP request object
            queryset: Selected user objects
        """
        updated = queryset.update(role=CustomUser.REGULAR)
        self.message_user(
            request,
            f'{updated} user(s) were demoted to regular user.'
        )
    make_regular.short_description = "Demote to regular user" 