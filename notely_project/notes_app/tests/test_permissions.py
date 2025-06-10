from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from notes_app.models import Note
from notes_app.permissions import IsOwner

User = get_user_model()


class IsOwnerPermissionTest(TestCase):
    """Test cases for the IsOwner permission"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = APIRequestFactory()
        self.permission = IsOwner()
        
        # Create test users
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123',
            role='regular'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123',
            role='regular'
        )
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='testpass123',
            role='admin'
        )
        
        # Create test notes
        self.note_user1 = Note.objects.create(
            user=self.user1,
            title='User1 Note',
            content='This note belongs to user1'
        )
        self.note_user2 = Note.objects.create(
            user=self.user2,
            title='User2 Note',
            content='This note belongs to user2'
        )
    
    def _create_request(self, user, method='GET'):
        """Helper method to create a request with a user"""
        request = getattr(self.factory, method.lower())('/')
        request.user = user
        return Request(request)
    
    def test_owner_can_access_own_note(self):
        """Test that a user can access their own note"""
        request = self._create_request(self.user1)
        
        has_permission = self.permission.has_object_permission(
            request, None, self.note_user1
        )
        
        self.assertTrue(has_permission)
    
    def test_owner_cannot_access_other_user_note(self):
        """Test that a user cannot access another user's note"""
        request = self._create_request(self.user1)
        
        has_permission = self.permission.has_object_permission(
            request, None, self.note_user2
        )
        
        self.assertFalse(has_permission)
    
    def test_different_user_cannot_access_note(self):
        """Test that user2 cannot access user1's note"""
        request = self._create_request(self.user2)
        
        has_permission = self.permission.has_object_permission(
            request, None, self.note_user1
        )
        
        self.assertFalse(has_permission)
    
    def test_admin_user_access_policy(self):
        """Test access for admin users (depends on implementation)"""
        request = self._create_request(self.admin_user)
        
        # Admin access policy depends on implementation
        # If IsOwner only checks ownership, admin should be denied
        # If there's special admin handling, admin should be allowed
        has_permission = self.permission.has_object_permission(
            request, None, self.note_user1
        )
        
        # Assuming IsOwner only checks direct ownership
        self.assertFalse(has_permission)
    
    def test_anonymous_user_denied(self):
        """Test that anonymous users are denied access"""
        from django.contrib.auth.models import AnonymousUser
        
        request = self._create_request(AnonymousUser())
        
        has_permission = self.permission.has_object_permission(
            request, None, self.note_user1
        )
        
        self.assertFalse(has_permission)
    
    def test_none_user_denied(self):
        """Test that request with None user is denied access"""
        request = self.factory.get('/')
        request.user = None
        request = Request(request)
        
        has_permission = self.permission.has_object_permission(
            request, None, self.note_user1
        )
        
        self.assertFalse(has_permission)
    
    def test_permission_with_different_methods(self):
        """Test that permission works consistently across HTTP methods"""
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        
        for method in methods:
            with self.subTest(method=method):
                request = self._create_request(self.user1, method)
                
                has_permission = self.permission.has_object_permission(
                    request, None, self.note_user1
                )
                
                self.assertTrue(has_permission)
    
    def test_permission_with_different_methods_wrong_user(self):
        """Test that permission denies access across all HTTP methods for wrong user"""
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        
        for method in methods:
            with self.subTest(method=method):
                request = self._create_request(self.user2, method)
                
                has_permission = self.permission.has_object_permission(
                    request, None, self.note_user1
                )
                
                self.assertFalse(has_permission)
    
    def test_permission_with_missing_user_attribute(self):
        """Test permission when note object doesn't have user attribute"""
        # Create a mock object without user attribute
        class MockObject:
            pass
        
        mock_obj = MockObject()
        request = self._create_request(self.user1)
        
        # This should raise AttributeError or handle gracefully
        with self.assertRaises(AttributeError):
            self.permission.has_object_permission(request, None, mock_obj)
    
    def test_has_permission_method_exists(self):
        """Test that has_permission method exists and can be called"""
        # Some permissions only implement has_object_permission
        # but it's good practice to also implement has_permission
        request = self._create_request(self.user1)
        
        # This should not raise an error
        try:
            result = self.permission.has_permission(request, None)
            # If implemented, it should return True for authenticated users
            # If not implemented, BasePermission returns True by default
            self.assertTrue(result)
        except NotImplementedError:
            # If not implemented, that's also acceptable for object-level permissions
            pass


class IsOwnerPermissionIntegrationTest(TestCase):
    """Integration tests for IsOwner permission with views"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = APIRequestFactory()
        
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123',
            role='regular'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123',
            role='regular'
        )
        
        self.note = Note.objects.create(
            user=self.user1,
            title='Test Note',
            content='Test content'
        )
    
    def test_permission_integration_with_view_context(self):
        """Test permission works correctly when used in a view context"""
        from unittest.mock import Mock
        
        # Mock a view
        mock_view = Mock()
        mock_view.action = 'retrieve'
        
        permission = IsOwner()
        
        # Test with correct user
        request = self._create_request(self.user1)
        has_permission = permission.has_object_permission(
            request, mock_view, self.note
        )
        self.assertTrue(has_permission)
        
        # Test with incorrect user
        request = self._create_request(self.user2)
        has_permission = permission.has_object_permission(
            request, mock_view, self.note
        )
        self.assertFalse(has_permission)
    
    def _create_request(self, user, method='GET'):
        """Helper method to create a request with a user"""
        request = getattr(self.factory, method.lower())('/')
        request.user = user
        return Request(request)
    
    def test_permission_with_view_actions(self):
        """Test permission with different view actions"""
        from unittest.mock import Mock
        
        actions = ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']
        permission = IsOwner()
        
        for action in actions:
            with self.subTest(action=action):
                mock_view = Mock()
                mock_view.action = action
                
                request = self._create_request(self.user1)
                has_permission = permission.has_object_permission(
                    request, mock_view, self.note
                )
                
                self.assertTrue(has_permission) 