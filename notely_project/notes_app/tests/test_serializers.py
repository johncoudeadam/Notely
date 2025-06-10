from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from notes_app.models import Note
from notes_app.serializers import NoteSerializer

User = get_user_model()


class NoteSerializerTest(TestCase):
    """Test cases for the NoteSerializer"""
    
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
            content='This is test content.'
        )
    
    def test_note_serialization(self):
        """Test serializing a Note object"""
        serializer = NoteSerializer(self.note)
        data = serializer.data
        
        self.assertEqual(data['id'], self.note.id)
        self.assertEqual(data['title'], 'Test Note')
        self.assertEqual(data['content'], 'This is test content.')
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        # User should not be included in serialized data for regular users
        self.assertNotIn('user', data)
    
    def test_note_deserialization_valid(self):
        """Test deserializing valid note data"""
        data = {
            'title': 'New Note Title',
            'content': 'New note content here.'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Test that validated data is correct
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['title'], 'New Note Title')
        self.assertEqual(validated_data['content'], 'New note content here.')
    
    def test_note_deserialization_missing_title(self):
        """Test deserializing note data without title"""
        data = {
            'content': 'Content without title'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_note_deserialization_missing_content(self):
        """Test deserializing note data without content"""
        data = {
            'title': 'Title without content'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)
    
    def test_note_deserialization_empty_title(self):
        """Test deserializing note data with empty title"""
        data = {
            'title': '',
            'content': 'Valid content'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_note_deserialization_empty_content(self):
        """Test deserializing note data with empty content"""
        data = {
            'title': 'Valid title',
            'content': ''
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)
    
    def test_note_deserialization_whitespace_only_title(self):
        """Test deserializing note data with whitespace-only title"""
        data = {
            'title': '   ',
            'content': 'Valid content'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_note_deserialization_whitespace_only_content(self):
        """Test deserializing note data with whitespace-only content"""
        data = {
            'title': 'Valid title',
            'content': '   '
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)
    
    def test_note_update_serialization(self):
        """Test updating an existing note"""
        data = {
            'title': 'Updated Title',
            'content': 'Updated content.'
        }
        
        serializer = NoteSerializer(self.note, data=data)
        self.assertTrue(serializer.is_valid())
        
        updated_note = serializer.save()
        
        self.assertEqual(updated_note.title, 'Updated Title')
        self.assertEqual(updated_note.content, 'Updated content.')
        self.assertEqual(updated_note.user, self.user1)  # User should remain the same
        self.assertGreater(updated_note.updated_at, self.note.updated_at)
    
    def test_note_partial_update_title_only(self):
        """Test partial update of note (title only)"""
        data = {
            'title': 'Partially Updated Title'
        }
        
        serializer = NoteSerializer(self.note, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_note = serializer.save()
        
        self.assertEqual(updated_note.title, 'Partially Updated Title')
        self.assertEqual(updated_note.content, 'This is test content.')  # Should remain unchanged
    
    def test_note_partial_update_content_only(self):
        """Test partial update of note (content only)"""
        data = {
            'content': 'Partially updated content.'
        }
        
        serializer = NoteSerializer(self.note, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_note = serializer.save()
        
        self.assertEqual(updated_note.title, 'Test Note')  # Should remain unchanged
        self.assertEqual(updated_note.content, 'Partially updated content.')
    
    def test_note_serializer_read_only_fields(self):
        """Test that certain fields are read-only"""
        data = {
            'id': 999,
            'title': 'Valid Title',
            'content': 'Valid content',
            'created_at': '2023-01-01T00:00:00Z',
            'updated_at': '2023-01-01T00:00:00Z'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # These fields should not be in validated_data as they are read-only
        validated_data = serializer.validated_data
        self.assertNotIn('id', validated_data)
        self.assertNotIn('created_at', validated_data)
        self.assertNotIn('updated_at', validated_data)
    
    def test_note_serializer_user_not_writable(self):
        """Test that user field cannot be set via serializer"""
        data = {
            'title': 'Valid Title',
            'content': 'Valid content',
            'user': self.user2.id  # Try to set different user
        }
        
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # User should not be in validated_data
        validated_data = serializer.validated_data
        self.assertNotIn('user', validated_data)
    
    def test_note_serializer_with_long_title(self):
        """Test serializer with title that exceeds max length"""
        long_title = 'x' * 201  # Assuming max_length=200
        data = {
            'title': long_title,
            'content': 'Valid content'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_note_serializer_with_special_characters(self):
        """Test serializer with special characters in title and content"""
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        data = {
            'title': f'Title with {special_chars}',
            'content': f'Content with {special_chars}'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        validated_data = serializer.validated_data
        self.assertIn(special_chars, validated_data['title'])
        self.assertIn(special_chars, validated_data['content'])
    
    def test_note_serializer_with_newlines(self):
        """Test serializer with newlines in title and content"""
        data = {
            'title': 'Title with\nnewlines',
            'content': 'Content with\nmultiple\nlines'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        validated_data = serializer.validated_data
        self.assertIn('\n', validated_data['title'])
        self.assertIn('\n', validated_data['content'])


class NoteSerializerContextTest(TestCase):
    """Test cases for NoteSerializer with context"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123',
            role='regular'
        )
    
    def test_note_serializer_with_request_context(self):
        """Test that serializer works correctly with request context"""
        request = self.factory.get('/')
        request.user = self.user
        
        data = {
            'title': 'Context Test Note',
            'content': 'Testing with request context'
        }
        
        serializer = NoteSerializer(
            data=data, 
            context={'request': Request(request)}
        )
        
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['title'], 'Context Test Note')
        self.assertEqual(validated_data['content'], 'Testing with request context')
    
    def test_note_serializer_without_context(self):
        """Test that serializer works without request context"""
        data = {
            'title': 'No Context Note',
            'content': 'Testing without context'
        }
        
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['title'], 'No Context Note')
        self.assertEqual(validated_data['content'], 'Testing without context') 