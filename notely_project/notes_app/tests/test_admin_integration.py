import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from notes_app.models import Note

User = get_user_model()


class AdminNoteAPIIntegrationTest(TestCase):
    """Integration tests for admin note management functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test users
        self.regular_user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123',
            role='regular'
        )
        self.regular_user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123',
            role='regular'
        )
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='testpass123',
            role='admin'
        )
        
        # Create test notes from different users
        self.note1 = Note.objects.create(
            user=self.regular_user1,
            title='User1 Note 1',
            content='Content from user1 first note'
        )
        self.note2 = Note.objects.create(
            user=self.regular_user1,
            title='User1 Note 2',
            content='Content from user1 second note'
        )
        self.note3 = Note.objects.create(
            user=self.regular_user2,
            title='User2 Note 1',
            content='Content from user2 note'
        )
        
        # Admin URLs (adjust based on your URL configuration)
        self.admin_notes_list_url = reverse('admin-note-list')
        self.admin_note_detail_url = lambda pk: reverse('admin-note-detail', kwargs={'pk': pk})
    
    def _authenticate_user(self, user):
        """Helper method to authenticate a user and set Authorization header"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return access_token
    
    def _clear_authentication(self):
        """Helper method to clear authentication"""
        self.client.credentials()


class AdminViewAllNotesTest(AdminNoteAPIIntegrationTest):
    """Test cases for admin viewing all notes"""
    
    def test_admin_can_view_all_notes(self):
        """Test that admin can view all notes from all users"""
        self._authenticate_user(self.admin_user)
        
        response = self.client.get(self.admin_notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        notes = data['results'] if 'results' in data else data
        
        # Admin should see all notes (3 total)
        self.assertEqual(len(notes), 3)
        
        # Verify all notes are present
        note_titles = [note['title'] for note in notes]
        self.assertIn('User1 Note 1', note_titles)
        self.assertIn('User1 Note 2', note_titles)
        self.assertIn('User2 Note 1', note_titles)
    
    def test_regular_user_cannot_access_admin_all_notes(self):
        """Test that regular users cannot access admin all notes endpoint"""
        self._authenticate_user(self.regular_user1)
        
        response = self.client.get(self.admin_notes_list_url)
        
        # Should be forbidden for regular users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_cannot_access_admin_notes(self):
        """Test that unauthenticated users cannot access admin notes"""
        response = self.client.get(self.admin_notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_view_all_notes_with_user_info(self):
        """Test that admin can see which user owns each note"""
        self._authenticate_user(self.admin_user)
        
        response = self.client.get(self.admin_notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        notes = data['results'] if 'results' in data else data
        
        # Find a specific note and verify user information is included
        user1_note = next(note for note in notes if note['title'] == 'User1 Note 1')
        
        # Depending on serializer implementation, user info might be included
        # This tests that admin serializer includes user information
        self.assertIn('user', user1_note)  # or 'user_email', depending on implementation


class AdminReadAnyNoteTest(AdminNoteAPIIntegrationTest):
    """Test cases for admin reading any specific note"""
    
    def test_admin_can_read_any_user_note(self):
        """Test that admin can read any user's note details"""
        self._authenticate_user(self.admin_user)
        
        # Admin reads user1's note
        response = self.client.get(self.admin_note_detail_url(self.note1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['id'], self.note1.id)
        self.assertEqual(data['title'], 'User1 Note 1')
        self.assertEqual(data['content'], 'Content from user1 first note')
    
    def test_admin_can_read_different_user_note(self):
        """Test that admin can read notes from different users"""
        self._authenticate_user(self.admin_user)
        
        # Admin reads user2's note
        response = self.client.get(self.admin_note_detail_url(self.note3.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['id'], self.note3.id)
        self.assertEqual(data['title'], 'User2 Note 1')
        self.assertEqual(data['content'], 'Content from user2 note')
    
    def test_regular_user_cannot_read_via_admin_endpoint(self):
        """Test that regular users cannot read notes via admin endpoint"""
        self._authenticate_user(self.regular_user1)
        
        response = self.client.get(self.admin_note_detail_url(self.note1.id))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminUpdateAnyNoteTest(AdminNoteAPIIntegrationTest):
    """Test cases for admin updating any user's note"""
    
    def test_admin_can_update_any_user_note(self):
        """Test that admin can update any user's note"""
        self._authenticate_user(self.admin_user)
        
        data = {
            'title': 'Admin Updated Title',
            'content': 'Admin updated this note content'
        }
        
        response = self.client.put(self.admin_note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Admin Updated Title')
        self.assertEqual(response_data['content'], 'Admin updated this note content')
        
        # Verify in database
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Admin Updated Title')
        self.assertEqual(self.note1.content, 'Admin updated this note content')
        # User should remain the same
        self.assertEqual(self.note1.user, self.regular_user1)
    
    def test_admin_can_partially_update_any_note(self):
        """Test that admin can partially update any user's note"""
        self._authenticate_user(self.admin_user)
        
        data = {
            'title': 'Admin Partial Update'
        }
        
        response = self.client.patch(self.admin_note_detail_url(self.note2.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the partial update
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Admin Partial Update')
        self.assertEqual(response_data['content'], 'Content from user1 second note')  # Should remain unchanged
        
        # Verify in database
        self.note2.refresh_from_db()
        self.assertEqual(self.note2.title, 'Admin Partial Update')
        self.assertEqual(self.note2.content, 'Content from user1 second note')
    
    def test_admin_update_different_user_note(self):
        """Test that admin can update notes from different users"""
        self._authenticate_user(self.admin_user)
        
        data = {
            'title': 'Admin Updated User2 Note',
            'content': 'Admin modified user2 note'
        }
        
        response = self.client.put(self.admin_note_detail_url(self.note3.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        self.note3.refresh_from_db()
        self.assertEqual(self.note3.title, 'Admin Updated User2 Note')
        self.assertEqual(self.note3.content, 'Admin modified user2 note')
        # User should remain the same
        self.assertEqual(self.note3.user, self.regular_user2)
    
    def test_regular_user_cannot_update_via_admin_endpoint(self):
        """Test that regular users cannot update notes via admin endpoint"""
        self._authenticate_user(self.regular_user1)
        
        data = {
            'title': 'Unauthorized Update',
            'content': 'This should not work'
        }
        
        response = self.client.put(self.admin_note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify note wasn't changed
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'User1 Note 1')
        self.assertEqual(self.note1.content, 'Content from user1 first note')


class AdminDeleteAnyNoteTest(AdminNoteAPIIntegrationTest):
    """Test cases for admin deleting any user's note"""
    
    def test_admin_can_delete_any_user_note(self):
        """Test that admin can delete any user's note"""
        self._authenticate_user(self.admin_user)
        
        note_id = self.note1.id
        
        response = self.client.delete(self.admin_note_detail_url(note_id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the note was deleted
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)
    
    def test_admin_can_delete_different_user_note(self):
        """Test that admin can delete notes from different users"""
        self._authenticate_user(self.admin_user)
        
        note_id = self.note3.id
        
        response = self.client.delete(self.admin_note_detail_url(note_id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the note was deleted
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)
    
    def test_regular_user_cannot_delete_via_admin_endpoint(self):
        """Test that regular users cannot delete notes via admin endpoint"""
        self._authenticate_user(self.regular_user1)
        
        response = self.client.delete(self.admin_note_detail_url(self.note1.id))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify note still exists
        self.assertTrue(Note.objects.filter(id=self.note1.id).exists())


class AdminNoteSearchAndFilterTest(AdminNoteAPIIntegrationTest):
    """Test cases for admin searching and filtering all notes"""
    
    def setUp(self):
        super().setUp()
        
        # Create additional notes for search testing
        Note.objects.create(
            user=self.regular_user1,
            title='Python Tutorial',
            content='Learning Python programming'
        )
        Note.objects.create(
            user=self.regular_user2,
            title='Django Guide',
            content='Django web framework guide'
        )
    
    def test_admin_search_all_notes(self):
        """Test that admin can search across all users' notes"""
        self._authenticate_user(self.admin_user)
        
        response = self.client.get(self.admin_notes_list_url, {'search': 'Python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        notes = data['results'] if 'results' in data else data
        
        # Should find the Python note regardless of which user created it
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['title'], 'Python Tutorial')
    
    def test_admin_search_by_user(self):
        """Test that admin can filter notes by specific user"""
        self._authenticate_user(self.admin_user)
        
        # Assuming there's a user filter parameter
        response = self.client.get(self.admin_notes_list_url, {'user': self.regular_user1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        notes = data['results'] if 'results' in data else data
        
        # Should only show notes from user1 (3 total including setup notes)
        self.assertEqual(len(notes), 3)
        
        # Verify all notes belong to user1
        for note in notes:
            if 'user' in note:
                self.assertEqual(note['user'], self.regular_user1.id)
    
    def test_admin_sort_all_notes(self):
        """Test that admin can sort all notes"""
        self._authenticate_user(self.admin_user)
        
        response = self.client.get(self.admin_notes_list_url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        notes = data['results'] if 'results' in data else data
        
        # Verify notes are sorted by title
        titles = [note['title'] for note in notes]
        self.assertEqual(titles, sorted(titles))


class AdminCreateNoteTest(AdminNoteAPIIntegrationTest):
    """Test cases for admin creating notes on behalf of users"""
    
    def test_admin_can_create_note_for_user(self):
        """Test that admin can create a note on behalf of a user"""
        self._authenticate_user(self.admin_user)
        
        data = {
            'title': 'Admin Created Note',
            'content': 'This note was created by admin for user1',
            'user': self.regular_user1.id  # Specify the user
        }
        
        response = self.client.post(self.admin_notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the note was created
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Admin Created Note')
        self.assertEqual(response_data['content'], 'This note was created by admin for user1')
        
        # Verify it's in the database and associated with the correct user
        note = Note.objects.get(id=response_data['id'])
        self.assertEqual(note.user, self.regular_user1)
        self.assertEqual(note.title, 'Admin Created Note')
    
    def test_admin_create_note_without_user_defaults_to_admin(self):
        """Test creating note without specifying user (if implementation allows)"""
        self._authenticate_user(self.admin_user)
        
        data = {
            'title': 'Admin Personal Note',
            'content': 'This is admin\'s own note'
        }
        
        response = self.client.post(self.admin_notes_list_url, data, format='json')
        
        # This test depends on implementation - might default to admin or require user field
        if response.status_code == status.HTTP_201_CREATED:
            response_data = response.json()
            note = Note.objects.get(id=response_data['id'])
            self.assertEqual(note.user, self.admin_user)
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # If user field is required
            self.assertIn('user', response.json())
    
    def test_regular_user_cannot_create_note_for_other_user(self):
        """Test that regular users cannot create notes for other users via admin endpoint"""
        self._authenticate_user(self.regular_user1)
        
        data = {
            'title': 'Malicious Note',
            'content': 'Trying to create note for another user',
            'user': self.regular_user2.id
        }
        
        response = self.client.post(self.admin_notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminNotePermissionEdgeCasesTest(AdminNoteAPIIntegrationTest):
    """Test edge cases and security aspects of admin note permissions"""
    
    def test_admin_cannot_transfer_note_ownership(self):
        """Test that admin cannot change note ownership via update"""
        self._authenticate_user(self.admin_user)
        
        data = {
            'title': 'Updated Title',
            'content': 'Updated content',
            'user': self.regular_user2.id  # Try to change ownership
        }
        
        response = self.client.put(self.admin_note_detail_url(self.note1.id), data, format='json')
        
        # Should succeed but not change ownership
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify ownership didn't change
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.user, self.regular_user1)  # Should still be original owner
        self.assertEqual(self.note1.title, 'Updated Title')    # But title should update
    
    def test_admin_access_nonexistent_note(self):
        """Test admin accessing a nonexistent note"""
        self._authenticate_user(self.admin_user)
        
        response = self.client.get(self.admin_note_detail_url(999999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_admin_operations_preserve_timestamps(self):
        """Test that admin operations properly update timestamps"""
        self._authenticate_user(self.admin_user)
        
        original_created_at = self.note1.created_at
        original_updated_at = self.note1.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        data = {
            'title': 'Admin Updated Title',
            'content': self.note1.content
        }
        
        response = self.client.put(self.admin_note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify timestamps
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.created_at, original_created_at)  # Should not change
        self.assertGreater(self.note1.updated_at, original_updated_at)  # Should update 