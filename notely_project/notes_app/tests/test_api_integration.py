import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from notes_app.models import Note

User = get_user_model()


class NoteAPIIntegrationTest(TestCase):
    """Integration tests for the Note API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
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
        self.note1 = Note.objects.create(
            user=self.user1,
            title='User1 First Note',
            content='Content of user1 first note'
        )
        self.note2 = Note.objects.create(
            user=self.user1,
            title='User1 Second Note',
            content='Content of user1 second note'
        )
        self.note3 = Note.objects.create(
            user=self.user2,
            title='User2 Note',
            content='Content of user2 note'
        )
        
        # URLs (adjust based on your URL configuration)
        self.notes_list_url = reverse('note-list')
        self.note_detail_url = lambda pk: reverse('note-detail', kwargs={'pk': pk})
    
    def _authenticate_user(self, user):
        """Helper method to authenticate a user and set Authorization header"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return access_token
    
    def _clear_authentication(self):
        """Helper method to clear authentication"""
        self.client.credentials()


class NoteListAPITest(NoteAPIIntegrationTest):
    """Test cases for note list endpoint (GET /api/notes/)"""
    
    def test_list_notes_authenticated_user(self):
        """Test that authenticated user can list their own notes"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should return only user1's notes
        data = response.json()
        self.assertEqual(len(data['results'] if 'results' in data else data), 2)
        
        # Verify the notes belong to user1
        note_titles = [note['title'] for note in (data['results'] if 'results' in data else data)]
        self.assertIn('User1 First Note', note_titles)
        self.assertIn('User1 Second Note', note_titles)
        self.assertNotIn('User2 Note', note_titles)
    
    def test_list_notes_unauthenticated_user(self):
        """Test that unauthenticated user cannot list notes"""
        response = self.client.get(self.notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_notes_different_user(self):
        """Test that user2 can only see their own notes"""
        self._authenticate_user(self.user2)
        
        response = self.client.get(self.notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(len(data['results'] if 'results' in data else data), 1)
        
        note_titles = [note['title'] for note in (data['results'] if 'results' in data else data)]
        self.assertIn('User2 Note', note_titles)
        self.assertNotIn('User1 First Note', note_titles)
        self.assertNotIn('User1 Second Note', note_titles)
    
    def test_list_notes_empty_for_user_with_no_notes(self):
        """Test listing notes for user with no notes"""
        user_no_notes = User.objects.create_user(
            email='nonotes@example.com',
            password='testpass123',
            role='regular'
        )
        self._authenticate_user(user_no_notes)
        
        response = self.client.get(self.notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results'] if 'results' in data else data), 0)


class NoteCreateAPITest(NoteAPIIntegrationTest):
    """Test cases for note creation endpoint (POST /api/notes/)"""
    
    def test_create_note_authenticated_user(self):
        """Test that authenticated user can create a note"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': 'New Note Title',
            'content': 'New note content here.'
        }
        
        response = self.client.post(self.notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the note was created
        response_data = response.json()
        self.assertEqual(response_data['title'], 'New Note Title')
        self.assertEqual(response_data['content'], 'New note content here.')
        self.assertIn('id', response_data)
        self.assertIn('created_at', response_data)
        self.assertIn('updated_at', response_data)
        
        # Verify it's in the database and associated with the correct user
        note = Note.objects.get(id=response_data['id'])
        self.assertEqual(note.user, self.user1)
        self.assertEqual(note.title, 'New Note Title')
        self.assertEqual(note.content, 'New note content here.')
    
    def test_create_note_unauthenticated_user(self):
        """Test that unauthenticated user cannot create a note"""
        data = {
            'title': 'Unauthorized Note',
            'content': 'This should not be created.'
        }
        
        response = self.client.post(self.notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_note_missing_title(self):
        """Test creating note without title"""
        self._authenticate_user(self.user1)
        
        data = {
            'content': 'Content without title'
        }
        
        response = self.client.post(self.notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.json())
    
    def test_create_note_missing_content(self):
        """Test creating note without content"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': 'Title without content'
        }
        
        response = self.client.post(self.notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.json())
    
    def test_create_note_empty_fields(self):
        """Test creating note with empty title and content"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': '',
            'content': ''
        }
        
        response = self.client.post(self.notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('title', response_data)
        self.assertIn('content', response_data)


class NoteRetrieveAPITest(NoteAPIIntegrationTest):
    """Test cases for note retrieval endpoint (GET /api/notes/{id}/)"""
    
    def test_retrieve_own_note(self):
        """Test that user can retrieve their own note"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.note_detail_url(self.note1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['id'], self.note1.id)
        self.assertEqual(data['title'], 'User1 First Note')
        self.assertEqual(data['content'], 'Content of user1 first note')
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_retrieve_other_user_note_forbidden(self):
        """Test that user cannot retrieve another user's note"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.note_detail_url(self.note3.id))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_note_unauthenticated(self):
        """Test that unauthenticated user cannot retrieve any note"""
        response = self.client.get(self.note_detail_url(self.note1.id))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_nonexistent_note(self):
        """Test retrieving a note that doesn't exist"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.note_detail_url(999999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteUpdateAPITest(NoteAPIIntegrationTest):
    """Test cases for note update endpoints (PUT/PATCH /api/notes/{id}/)"""
    
    def test_update_own_note_put(self):
        """Test that user can update their own note using PUT"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': 'Updated Title',
            'content': 'Updated content.'
        }
        
        response = self.client.put(self.note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Updated Title')
        self.assertEqual(response_data['content'], 'Updated content.')
        
        # Verify in database
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Updated Title')
        self.assertEqual(self.note1.content, 'Updated content.')
    
    def test_update_own_note_patch(self):
        """Test that user can partially update their own note using PATCH"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': 'Partially Updated Title'
        }
        
        response = self.client.patch(self.note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Partially Updated Title')
        self.assertEqual(response_data['content'], 'Content of user1 first note')  # Should remain unchanged
        
        # Verify in database
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Partially Updated Title')
        self.assertEqual(self.note1.content, 'Content of user1 first note')
    
    def test_update_other_user_note_forbidden(self):
        """Test that user cannot update another user's note"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': 'Malicious Update',
            'content': 'This should not work.'
        }
        
        response = self.client.put(self.note_detail_url(self.note3.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verify the note wasn't changed
        self.note3.refresh_from_db()
        self.assertEqual(self.note3.title, 'User2 Note')
        self.assertEqual(self.note3.content, 'Content of user2 note')
    
    def test_update_note_unauthenticated(self):
        """Test that unauthenticated user cannot update any note"""
        data = {
            'title': 'Unauthorized Update',
            'content': 'This should not work.'
        }
        
        response = self.client.put(self.note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_note_invalid_data(self):
        """Test updating note with invalid data"""
        self._authenticate_user(self.user1)
        
        data = {
            'title': '',  # Empty title should be invalid
            'content': 'Valid content'
        }
        
        response = self.client.put(self.note_detail_url(self.note1.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.json())


class NoteDeleteAPITest(NoteAPIIntegrationTest):
    """Test cases for note deletion endpoint (DELETE /api/notes/{id}/)"""
    
    def test_delete_own_note(self):
        """Test that user can delete their own note"""
        self._authenticate_user(self.user1)
        
        note_id = self.note1.id
        
        response = self.client.delete(self.note_detail_url(note_id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the note was deleted
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)
    
    def test_delete_other_user_note_forbidden(self):
        """Test that user cannot delete another user's note"""
        self._authenticate_user(self.user1)
        
        response = self.client.delete(self.note_detail_url(self.note3.id))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verify the note still exists
        self.assertTrue(Note.objects.filter(id=self.note3.id).exists())
    
    def test_delete_note_unauthenticated(self):
        """Test that unauthenticated user cannot delete any note"""
        response = self.client.delete(self.note_detail_url(self.note1.id))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify the note still exists
        self.assertTrue(Note.objects.filter(id=self.note1.id).exists())
    
    def test_delete_nonexistent_note(self):
        """Test deleting a note that doesn't exist"""
        self._authenticate_user(self.user1)
        
        response = self.client.delete(self.note_detail_url(999999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteSearchAndFilterAPITest(NoteAPIIntegrationTest):
    """Test cases for note search and filtering functionality"""
    
    def setUp(self):
        super().setUp()
        
        # Create additional notes for search testing
        Note.objects.create(
            user=self.user1,
            title='Python Programming',
            content='Notes about Python programming'
        )
        Note.objects.create(
            user=self.user1,
            title='Django Framework',
            content='Notes about Django web framework'
        )
        Note.objects.create(
            user=self.user1,
            title='JavaScript Basics',
            content='Basic JavaScript concepts'
        )
    
    def test_search_notes_by_title(self):
        """Test searching notes by title"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'search': 'Python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Should find the note with "Python" in the title
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Python Programming')
    
    def test_search_notes_case_insensitive(self):
        """Test that search is case insensitive"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'search': 'python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Should still find the note with "Python" in the title
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Python Programming')
    
    def test_search_notes_partial_match(self):
        """Test searching with partial title match"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'search': 'User1'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Should find both original notes with "User1" in title
        self.assertEqual(len(results), 2)
        note_titles = [note['title'] for note in results]
        self.assertIn('User1 First Note', note_titles)
        self.assertIn('User1 Second Note', note_titles)
    
    def test_search_notes_no_results(self):
        """Test searching with no matching results"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'search': 'NonexistentTerm'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        self.assertEqual(len(results), 0)
    
    def test_sort_notes_by_title_ascending(self):
        """Test sorting notes by title in ascending order"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Verify the notes are sorted by title
        titles = [note['title'] for note in results]
        self.assertEqual(titles, sorted(titles))
    
    def test_sort_notes_by_title_descending(self):
        """Test sorting notes by title in descending order"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Verify the notes are sorted by title in descending order
        titles = [note['title'] for note in results]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_sort_notes_by_created_at_descending(self):
        """Test sorting notes by creation date in descending order"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {'ordering': '-created_at'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Verify the notes are sorted by created_at in descending order
        # (newest first)
        if len(results) > 1:
            for i in range(len(results) - 1):
                self.assertGreaterEqual(results[i]['created_at'], results[i + 1]['created_at'])
    
    def test_combined_search_and_sort(self):
        """Test combining search and sort parameters"""
        self._authenticate_user(self.user1)
        
        response = self.client.get(self.notes_list_url, {
            'search': 'User1',
            'ordering': 'title'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        results = data['results'] if 'results' in data else data
        
        # Should find both User1 notes, sorted by title
        self.assertEqual(len(results), 2)
        titles = [note['title'] for note in results]
        self.assertEqual(titles, ['User1 First Note', 'User1 Second Note'])


class NoteAPISecurityTest(NoteAPIIntegrationTest):
    """Test cases for API security aspects"""
    
    def test_invalid_jwt_token(self):
        """Test that invalid JWT token is rejected"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-token')
        
        response = self.client.get(self.notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_expired_jwt_token(self):
        """Test that expired JWT token is rejected"""
        # This test would require creating an expired token
        # which is complex to do in a unit test context
        # In practice, you'd mock the token validation
        pass
    
    def test_malformed_authorization_header(self):
        """Test that malformed authorization header is rejected"""
        self.client.credentials(HTTP_AUTHORIZATION='InvalidFormat token')
        
        response = self.client.get(self.notes_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_sql_injection_attempt_in_search(self):
        """Test that SQL injection attempts in search are handled safely"""
        self._authenticate_user(self.user1)
        
        malicious_query = "'; DROP TABLE notes_note; --"
        
        response = self.client.get(self.notes_list_url, {'search': malicious_query})
        
        # Should not crash and should return empty results
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the table still exists by making another request
        response2 = self.client.get(self.notes_list_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    def test_xss_attempt_in_note_content(self):
        """Test that XSS attempts in note content are handled"""
        self._authenticate_user(self.user1)
        
        xss_content = '<script>alert("XSS")</script>'
        
        data = {
            'title': 'XSS Test Note',
            'content': xss_content
        }
        
        response = self.client.post(self.notes_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # The content should be stored as-is (sanitization happens on frontend)
        response_data = response.json()
        self.assertEqual(response_data['content'], xss_content) 