from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from notes_app.models import Note

User = get_user_model()


class NoteModelTest(TestCase):
    """Test cases for the Note model"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_note_creation_valid(self):
        """Test creating a valid note"""
        note = Note.objects.create(
            user=self.user1,
            title='Test Note',
            content='This is a test note content.'
        )
        
        self.assertEqual(note.user, self.user1)
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is a test note content.')
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)
        self.assertEqual(note.created_at, note.updated_at)
    
    def test_note_title_required(self):
        """Test that title is required"""
        with self.assertRaises(ValidationError):
            note = Note(
                user=self.user1,
                title='',
                content='Content without title'
            )
            note.full_clean()
    
    def test_note_content_required(self):
        """Test that content is required"""
        with self.assertRaises(ValidationError):
            note = Note(
                user=self.user1,
                title='Title without content',
                content=''
            )
            note.full_clean()
    
    def test_note_user_required(self):
        """Test that user is required"""
        with self.assertRaises(IntegrityError):
            Note.objects.create(
                title='Orphan Note',
                content='This note has no user'
            )
    
    def test_note_title_max_length(self):
        """Test title max length constraint"""
        long_title = 'x' * 201  # Assuming max_length=200
        with self.assertRaises(ValidationError):
            note = Note(
                user=self.user1,
                title=long_title,
                content='Valid content'
            )
            note.full_clean()
    
    def test_note_updated_at_auto_update(self):
        """Test that updated_at is automatically updated on save"""
        note = Note.objects.create(
            user=self.user1,
            title='Original Title',
            content='Original content'
        )
        original_updated_at = note.updated_at
        
        # Wait a small amount and update
        import time
        time.sleep(0.01)
        
        note.title = 'Updated Title'
        note.save()
        
        note.refresh_from_db()
        self.assertGreater(note.updated_at, original_updated_at)
    
    def test_note_str_method(self):
        """Test the string representation of a note"""
        note = Note.objects.create(
            user=self.user1,
            title='Test Note Title',
            content='Test content'
        )
        
        expected_str = f'Test Note Title - {self.user1.email}'
        self.assertEqual(str(note), expected_str)
    
    def test_note_user_relationship(self):
        """Test the foreign key relationship to User"""
        note = Note.objects.create(
            user=self.user1,
            title='Relationship Test',
            content='Testing user relationship'
        )
        
        # Test forward relationship
        self.assertEqual(note.user, self.user1)
        
        # Test reverse relationship
        user_notes = self.user1.notes.all()
        self.assertIn(note, user_notes)
        self.assertEqual(user_notes.count(), 1)
    
    def test_multiple_notes_same_user(self):
        """Test that a user can have multiple notes"""
        note1 = Note.objects.create(
            user=self.user1,
            title='First Note',
            content='First note content'
        )
        note2 = Note.objects.create(
            user=self.user1,
            title='Second Note',
            content='Second note content'
        )
        
        user_notes = self.user1.notes.all()
        self.assertEqual(user_notes.count(), 2)
        self.assertIn(note1, user_notes)
        self.assertIn(note2, user_notes)
    
    def test_notes_different_users(self):
        """Test that notes are properly isolated by user"""
        note1 = Note.objects.create(
            user=self.user1,
            title='User1 Note',
            content='Content for user1'
        )
        note2 = Note.objects.create(
            user=self.user2,
            title='User2 Note',
            content='Content for user2'
        )
        
        user1_notes = self.user1.notes.all()
        user2_notes = self.user2.notes.all()
        
        self.assertEqual(user1_notes.count(), 1)
        self.assertEqual(user2_notes.count(), 1)
        self.assertIn(note1, user1_notes)
        self.assertNotIn(note2, user1_notes)
        self.assertIn(note2, user2_notes)
        self.assertNotIn(note1, user2_notes)
    
    def test_note_cascade_delete_user(self):
        """Test that notes are deleted when user is deleted"""
        note = Note.objects.create(
            user=self.user1,
            title='Will be deleted',
            content='This note will be deleted with user'
        )
        note_id = note.id
        
        # Delete the user
        self.user1.delete()
        
        # Note should also be deleted
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)
    
    def test_note_ordering(self):
        """Test default ordering of notes"""
        # Create notes with different timestamps
        note1 = Note.objects.create(
            user=self.user1,
            title='First Note',
            content='First content'
        )
        
        # Create second note slightly later
        import time
        time.sleep(0.01)
        
        note2 = Note.objects.create(
            user=self.user1,
            title='Second Note',
            content='Second content'
        )
        
        notes = Note.objects.filter(user=self.user1)
        
        # Should be ordered by created_at descending by default (if specified in Meta)
        # This test depends on the actual ordering specified in the model
        self.assertEqual(list(notes), [note2, note1])  # Assuming -created_at ordering


class NoteModelValidationTest(TestCase):
    """Test cases for Note model field validation"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            role='regular'
        )
    
    def test_note_with_whitespace_only_title(self):
        """Test that whitespace-only title is invalid"""
        with self.assertRaises(ValidationError):
            note = Note(
                user=self.user,
                title='   ',
                content='Valid content'
            )
            note.full_clean()
    
    def test_note_with_whitespace_only_content(self):
        """Test that whitespace-only content is invalid"""
        with self.assertRaises(ValidationError):
            note = Note(
                user=self.user,
                title='Valid title',
                content='   '
            )
            note.full_clean()
    
    def test_note_with_newlines_in_title_and_content(self):
        """Test that newlines are allowed in title and content"""
        note = Note.objects.create(
            user=self.user,
            title='Title with\nnewline',
            content='Content with\nmultiple\nlines'
        )
        
        self.assertIn('\n', note.title)
        self.assertIn('\n', note.content)
    
    def test_note_with_special_characters(self):
        """Test that special characters are allowed"""
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        note = Note.objects.create(
            user=self.user,
            title=f'Special chars: {special_chars}',
            content=f'Content with special chars: {special_chars}'
        )
        
        self.assertIn(special_chars, note.title)
        self.assertIn(special_chars, note.content) 