# Testing Guide for Simple Note Taking App

This document provides a comprehensive guide to the testing strategy and implementation for the Simple Note Taking App.

## Test Strategy Overview

The testing strategy follows a layered approach covering:

### 1. Unit Tests
**Purpose**: Test individual components in isolation
- **Models**: Data validation, relationships, business logic
- **Serializers**: Data serialization/deserialization, validation
- **Permissions**: Access control logic
- **Utilities**: Helper functions and custom methods

### 2. Integration Tests  
**Purpose**: Test complete functionality with real API calls
- **API Endpoints**: Full request-response cycles
- **Authentication**: JWT token handling
- **Cross-user Security**: Ensure data isolation
- **Search & Filtering**: Query functionality
- **Admin Operations**: Administrative capabilities

## Test Structure

```
notely_project/
├── notes_app/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py              # Unit tests for Note model
│       ├── test_serializers.py         # Unit tests for NoteSerializer
│       ├── test_permissions.py         # Unit tests for IsOwner permission
│       ├── test_api_integration.py     # Integration tests for regular users
│       └── test_admin_integration.py   # Integration tests for admin users
├── users/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py              # Unit tests for User model
│       └── test_serializers.py         # Unit tests for User serializers
├── run_tests.py                        # Custom test runner script
└── TESTING.md                          # This document
```

## Running Tests

### Prerequisites

1. **Install test dependencies**:
   ```bash
   pip install coverage factory-boy pytest-django
   ```

2. **Set up test database**:
   ```bash
   python manage.py migrate --settings=notely_project.settings
   ```

### Basic Test Commands

#### Using Django's built-in test runner:

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test notes_app

# Run specific test class
python manage.py test notes_app.tests.test_models.NoteModelTest

# Run specific test method
python manage.py test notes_app.tests.test_models.NoteModelTest.test_note_creation_valid

# Run with verbose output
python manage.py test --verbosity=2

# Keep test database between runs (faster)
python manage.py test --keepdb
```

#### Using the custom test runner:

```bash
# Run only unit tests
python run_tests.py --unit

# Run only integration tests  
python run_tests.py --integration

# Run all tests
python run_tests.py --all

# Run tests with coverage report
python run_tests.py --coverage

# Run tests for specific app
python run_tests.py --app notes_app

# Run specific test class
python run_tests.py --class NoteModelTest

# Run with verbose output
python run_tests.py --verbose

# Run tests in parallel (faster)
python run_tests.py --parallel 4

# Stop on first failure
python run_tests.py --failfast
```

### Coverage Reports

Generate detailed coverage reports to identify untested code:

```bash
# Run tests with coverage
python run_tests.py --coverage

# Or using coverage directly
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report in htmlcov/
```

## Test Categories Explained

### Unit Tests

#### Model Tests (`test_models.py`)
Tests for the `Note` model covering:

- **Field Validation**: Required fields, max lengths, data types
- **Relationships**: Foreign key to User, cascade behavior
- **Model Methods**: String representation, custom methods
- **Database Constraints**: Unique constraints, validation rules
- **Edge Cases**: Empty values, special characters, Unicode

**Key Test Classes**:
- `NoteModelTest`: Core model functionality
- `NoteModelValidationTest`: Field validation and constraints

#### Serializer Tests (`test_serializers.py`)
Tests for the `NoteSerializer` covering:

- **Serialization**: Converting model instances to JSON
- **Deserialization**: Converting JSON to model instances
- **Validation**: Field-level and object-level validation
- **Read-only Fields**: Ensuring certain fields cannot be modified
- **Context Handling**: Request context and user information

**Key Test Classes**:
- `NoteSerializerTest`: Core serialization functionality
- `NoteSerializerContextTest`: Context-dependent behavior

#### Permission Tests (`test_permissions.py`)
Tests for custom permission classes:

- **Object-level Permissions**: User can only access their own notes
- **Method Permissions**: Different permissions for different HTTP methods
- **Edge Cases**: Anonymous users, missing attributes
- **Integration**: Permission behavior in view context

**Key Test Classes**:
- `IsOwnerPermissionTest`: Core permission logic
- `IsOwnerPermissionIntegrationTest`: Permission with views

### Integration Tests

#### API Integration Tests (`test_api_integration.py`)
Tests for complete API functionality covering:

- **CRUD Operations**: Create, Read, Update, Delete notes
- **Authentication**: JWT token handling and validation
- **Authorization**: User isolation and access control
- **Search & Filter**: Query parameters and results
- **Error Handling**: Various error scenarios
- **Security**: SQL injection, XSS attempts

**Key Test Classes**:
- `NoteListAPITest`: GET /api/notes/
- `NoteCreateAPITest`: POST /api/notes/
- `NoteRetrieveAPITest`: GET /api/notes/{id}/
- `NoteUpdateAPITest`: PUT/PATCH /api/notes/{id}/
- `NoteDeleteAPITest`: DELETE /api/notes/{id}/
- `NoteSearchAndFilterAPITest`: Search and sorting functionality
- `NoteAPISecurityTest`: Security-related tests

#### Admin Integration Tests (`test_admin_integration.py`)
Tests for administrator functionality covering:

- **View All Notes**: Admin can see notes from all users
- **CRUD Any Note**: Admin can modify any user's notes
- **User Management**: Creating notes on behalf of users
- **Admin Permissions**: Ensuring regular users cannot access admin endpoints
- **Data Integrity**: Ensuring admin operations don't corrupt data

**Key Test Classes**:
- `AdminViewAllNotesTest`: Admin viewing all notes
- `AdminReadAnyNoteTest`: Admin reading specific notes
- `AdminUpdateAnyNoteTest`: Admin modifying notes
- `AdminDeleteAnyNoteTest`: Admin deleting notes
- `AdminNoteSearchAndFilterTest`: Admin search functionality
- `AdminCreateNoteTest`: Admin creating notes for users
- `AdminNotePermissionEdgeCasesTest`: Edge cases and security

## Test Data Management

### Test Fixtures
- Use Django's built-in fixtures or Factory Boy for consistent test data
- Each test class has its own `setUp()` method for test isolation
- Common helper methods for authentication and data creation

### Test Database
- Uses separate test database (automatically created/destroyed)
- Use `--keepdb` flag for faster consecutive test runs
- Test data is isolated between test methods

## Best Practices

### Writing Tests

1. **Test Organization**:
   - One test file per module/component
   - Group related tests in test classes
   - Use descriptive test method names

2. **Test Independence**:
   - Each test should be independent and isolated
   - Use `setUp()` and `tearDown()` methods properly
   - Don't rely on test execution order

3. **Test Coverage**:
   - Aim for high code coverage (>90%)
   - Test both happy path and error scenarios
   - Include edge cases and boundary conditions

4. **Assertions**:
   - Use specific assertions (`assertEqual`, `assertIn`, etc.)
   - Include meaningful assertion messages
   - Test both positive and negative cases

### Authentication in Tests

```python
def _authenticate_user(self, user):
    """Helper method to authenticate a user"""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return access_token
```

### Common Test Patterns

#### Testing API Endpoints:
```python
def test_create_note_success(self):
    self._authenticate_user(self.user)
    
    data = {'title': 'Test Note', 'content': 'Test content'}
    response = self.client.post(self.notes_url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.json()['title'], 'Test Note')
    
    # Verify in database
    note = Note.objects.get(id=response.json()['id'])
    self.assertEqual(note.user, self.user)
```

#### Testing Permissions:
```python
def test_user_cannot_access_other_note(self):
    self._authenticate_user(self.user1)
    
    response = self.client.get(f'/api/notes/{self.user2_note.id}/')
    
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
```

## Continuous Integration

For CI/CD pipelines, use these commands:

```bash
# Run all tests with coverage (CI environment)
python run_tests.py --coverage --failfast --parallel 2

# Generate coverage report for CI
coverage xml  # For tools like Codecov
coverage json # For programmatic access
```

## Performance Considerations

### Optimizing Test Execution

1. **Use `--keepdb`**: Reuse test database between runs
2. **Parallel Execution**: Use `--parallel` for faster execution
3. **Test Selection**: Run only relevant tests during development
4. **Database Transactions**: Tests run in transactions (automatic rollback)

### Test Database Settings

For faster tests, consider these settings in `settings.py`:

```python
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
    
    # Disable migrations for faster test setup
    MIGRATION_MODULES = {
        'notes_app': None,
        'users': None,
    }
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `DJANGO_SETTINGS_MODULE` is set correctly
2. **Database Errors**: Run migrations on test database
3. **Authentication Errors**: Check JWT settings and token generation
4. **Permission Errors**: Verify user roles and permission classes

### Debug Test Failures

```bash
# Run specific failing test with verbose output
python manage.py test notes_app.tests.test_models.NoteModelTest.test_failing_test --verbosity=2

# Use pdb for debugging
import pdb; pdb.set_trace()  # Add to test code

# Check test database state
python manage.py dbshell --settings=test_settings
```

## Monitoring and Metrics

### Coverage Goals
- **Overall Coverage**: >90%
- **Model Coverage**: >95% (critical business logic)
- **View Coverage**: >85% (API endpoints)
- **Permission Coverage**: >95% (security critical)

### Test Metrics to Track
- Total number of tests
- Test execution time
- Coverage percentage
- Number of failing tests
- Test reliability (flaky tests)

This comprehensive testing strategy ensures the Simple Note Taking App is robust, secure, and maintainable while providing confidence in all functionality from individual components to complete user workflows. 