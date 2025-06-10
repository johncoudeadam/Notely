"""
@description
User models for the Simple Note Taking App.
This module defines the CustomUser model that extends Django's AbstractUser
to include additional fields for role-based access control and timestamps.

Key features:
- Role-based access control (regular users and administrators)
- Email-based authentication instead of username
- Automatic timestamp tracking for creation and updates
- Built-in active/inactive status management

@dependencies
- django.contrib.auth.models: Django's built-in user authentication models
- django.db: Django's database models framework

@notes
- Uses email as the primary identifier for authentication (USERNAME_FIELD)
- Role field restricts users to 'regular' or 'admin' roles
- Inherits all standard Django user functionality (permissions, groups, etc.)
- created_at and updated_at fields automatically track record lifecycle
"""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """
    Custom user manager for handling email-based authentication.
    
    This manager provides methods to create users and superusers
    using email as the primary identifier instead of username.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        
        Args:
            email (str): User's email address
            password (str): User's password
            **extra_fields: Additional fields for the user
            
        Returns:
            CustomUser: The created user instance
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        
        Args:
            email (str): Superuser's email address
            password (str): Superuser's password
            **extra_fields: Additional fields for the user
            
        Returns:
            CustomUser: The created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    This model provides role-based access control and uses email
    as the primary authentication field instead of username.
    
    Attributes:
        email (EmailField): Primary identifier for authentication, must be unique
        role (CharField): User role, either 'regular' or 'admin'
        is_active (BooleanField): Whether the user account is active (inherited from AbstractUser)
        created_at (DateTimeField): Timestamp when the user was created
        updated_at (DateTimeField): Timestamp when the user was last updated
        
    Role Choices:
        REGULAR: Standard user with access to personal notes only
        ADMIN: Administrator with access to user management and all notes
    """
    
    # Role choices for user types
    REGULAR = 'regular'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (REGULAR, 'Regular User'),
        (ADMIN, 'Administrator'),
    ]
    
    # Override email field to be required and unique
    email = models.EmailField(
        unique=True,
        help_text='Required. Enter a valid email address.'
    )
    
    # Role field to distinguish between regular users and administrators
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=REGULAR,
        help_text='Designates the user role and permissions level.'
    )
    
    # Timestamp fields for tracking record lifecycle
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when the user account was created.'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when the user account was last updated.'
    )
    
    # Set email as the field used for authentication
    USERNAME_FIELD = 'email'
    
    # Remove email from required fields since it's now the USERNAME_FIELD
    REQUIRED_FIELDS = []
    
    # Use the custom user manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        """
        Return string representation of the user.
        
        Returns:
            str: User's email address
        """
        return self.email
    
    def is_admin(self):
        """
        Check if the user has administrator privileges.
        
        Returns:
            bool: True if user is an administrator, False otherwise
        """
        return self.role == self.ADMIN
    
    def is_regular_user(self):
        """
        Check if the user is a regular user.
        
        Returns:
            bool: True if user is a regular user, False otherwise
        """
        return self.role == self.REGULAR 