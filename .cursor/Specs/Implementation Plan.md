# Implementation Plan

## Phase 0: Initial Project Setup & Configuration

- [ ] Step 1: Initialize Django Project and Configure Basic Settings
    - **Task**: Create a new Django project named `notely_project`. Initialize a Git repository. Create a `.gitignore` file suitable for Python/Django projects. Configure basic settings like `TIME_ZONE`.
    - **Files**:
        - `notely_project/manage.py`
        - `notely_project/notely_project/settings.py`: Modify `INSTALLED_APPS`, `MIDDLEWARE`, `TIME_ZONE`.
        - `notely_project/notely_project/urls.py`
        - `notely_project/notely_project/asgi.py`
        - `notely_project/notely_project/wsgi.py`
        - `notely_project/.gitignore`: Add common Python, Django, and OS-specific ignores.
        - `notely_project/requirements.txt`: Add `Django`, `psycopg2-binary`.
    - **Step Dependencies**: None
    - **User Instructions**:
        1.  `python -m venv venv`
        2.  `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
        3.  `pip install Django psycopg2-binary`
        4.  `django-admin startproject notely_project .` (run inside the git repo root)
        5.  `git init`
        6.  Create and populate `.gitignore`.
        7.  `pip freeze > requirements.txt`

- [ ] Step 2: Configure PostgreSQL Database Connection (Placeholder)
    - **Task**: Update `settings.py` to use PostgreSQL. Use environment variables for database credentials. For local development, provide default values or instructions for setting up a local PostgreSQL instance.
    - **Files**:
        - `notely_project/notely_project/settings.py`: Modify the `DATABASES` setting.
    - **Step Dependencies**: Step 1
    - **User Instructions**:
        1.  Ensure PostgreSQL is installed and a database is created for this project.
        2.  Set the following environment variables (e.g., in a `.env` file, though Django doesn't natively support them without an extra package like `python-dotenv` which we can add now):
            * `DB_NAME`
            * `DB_USER`
            * `DB_PASSWORD`
            * `DB_HOST`
            * `DB_PORT`
        3.  (Optional) Install `python-dotenv`: `pip install python-dotenv` and add it to `requirements.txt`. Update `manage.py` and `wsgi.py`/`asgi.py` to load `.env` if used.

- [ ] Step 3: Initialize Vite + React + TypeScript Frontend Project
    - **Task**: Create a new Vite project with React and TypeScript named `notely_frontend`. Initialize a Git repository (or use the parent one if it's a monorepo, but for simplicity, assume separate for now, or within the same main project dir).
    - **Files**: Standard Vite + React + TS project structure.
        - `notely_frontend/package.json`
        - `notely_frontend/vite.config.ts`
        - `notely_frontend/tsconfig.json`
        - `notely_frontend/src/main.tsx`
        - `notely_frontend/src/App.tsx`
        - `notely_frontend/.gitignore`: Add common Node, React ignores.
    - **Step Dependencies**: None
    - **User Instructions**:
        1.  `npm create vite@latest notely_frontend -- --template react-ts`
        2.  `cd notely_frontend`
        3.  `npm install`
        4.  (If not already in a parent git repo) `git init` and create `.gitignore`.

- [ ] Step 4: Install and Configure Tailwind CSS for Frontend
    - **Task**: Install Tailwind CSS, PostCSS, and Autoprefixer. Initialize Tailwind CSS configuration. Configure template paths in `tailwind.config.js`. Include Tailwind directives in `index.css`.
    - **Files**:
        - `notely_frontend/package.json`: Add dependencies.
        - `notely_frontend/tailwind.config.js`: Create and configure.
        - `notely_frontend/postcss.config.js`: Create and configure.
        - `notely_frontend/src/index.css`: Add Tailwind directives.
    - **Step Dependencies**: Step 3
    - **User Instructions**:
        1.  `cd notely_frontend`
        2.  `npm install -D tailwindcss postcss autoprefixer`
        3.  `npx tailwindcss init -p`
        4.  Configure `content` in `tailwind.config.js` to include `src/**/*.{js,jsx,ts,tsx}`.
        5.  Add `@tailwind base; @tailwind components; @tailwind utilities;` to `src/index.css`.

## Phase 1: Core Backend - Models and Admin

- [ ] Step 5: Create `users` Django App and Custom User Model
    - **Task**: Create a Django app named `users`. Define a custom `User` model inheriting from `AbstractUser` to include `role` (`regular`, `admin`), `is_active`, `created_at`, `updated_at` fields. Set `email` as `USERNAME_FIELD`.
    - **Files**:
        - `notely_project/users/apps.py`
        - `notely_project/users/models.py`: Define `CustomUser` model.
        - `notely_project/users/admin.py`
        - `notely_project/notely_project/settings.py`: Add `users` to `INSTALLED_APPS` and set `AUTH_USER_MODEL = 'users.CustomUser'`.
    - **Step Dependencies**: Step 1, Step 2
    - **User Instructions**:
        1.  `python manage.py startapp users`
        2.  Update `settings.py` as described.

- [ ] Step 6: Create `notes_app` Django App and Note Model
    - **Task**: Create a Django app named `notes_app`. Define the `Note` model with `user_id` (ForeignKey to `CustomUser`), `title`, `content`, `created_at`, `updated_at` fields.
    - **Files**:
        - `notely_project/notes_app/apps.py`
        - `notely_project/notes_app/models.py`: Define `Note` model.
        - `notely_project/notes_app/admin.py`
        - `notely_project/notely_project/settings.py`: Add `notes_app` to `INSTALLED_APPS`.
    - **Step Dependencies**: Step 5
    - **User Instructions**:
        1.  `python manage.py startapp notes_app`
        2.  Update `settings.py` as described.

- [ ] Step 7: Create Database Migrations for User and Note Models
    - **Task**: Generate and apply database migrations for the `users` and `notes_app` models.
    - **Files**:
        - `notely_project/users/migrations/0001_initial.py` (auto-generated)
        - `notely_project/notes_app/migrations/0001_initial.py` (auto-generated)
    - **Step Dependencies**: Step 5, Step 6
    - **User Instructions**:
        1.  `python manage.py makemigrations users notes_app`
        2.  `python manage.py migrate`

- [ ] Step 8: Configure Django Admin for User and Note Models
    - **Task**: Register `CustomUser` and `Note` models with the Django admin site. Customize `UserAdmin` to display `email`, `role`, `is_active`.
    - **Files**:
        - `notely_project/users/admin.py`: Register `CustomUser` with a custom `UserAdmin`.
        - `notely_project/notes_app/admin.py`: Register `Note` model.
    - **Step Dependencies**: Step 5, Step 6, Step 7
    - **User Instructions**:
        1.  Create an initial admin user: `python manage.py createsuperuser` (Follow prompts: email, password). This fulfills US-001.
        2.  Run the development server: `python manage.py runserver`.
        3.  Navigate to `/admin` and log in to verify user and note management (initial part of US-002).

## Phase 2: Backend - API Foundation & User Authentication

- [ ] Step 9: Install and Configure DRF, SimpleJWT, and DRF-Spectacular
    - **Task**: Install Django Rest Framework (DRF), DRF SimpleJWT (for JWT authentication), and `drf-spectacular` (for OpenAPI schema generation). Configure them in `settings.py`.
    - **Files**:
        - `notely_project/requirements.txt`: Add `djangorestframework`, `djangorestframework-simplejwt`, `drf-spectacular`.
        - `notely_project/notely_project/settings.py`: Add `rest_framework`, `rest_framework_simplejwt`, `drf_spectacular` to `INSTALLED_APPS`. Configure `REST_FRAMEWORK` for default authentication classes (JWT) and `drf_spectacular` settings.
    - **Step Dependencies**: Step 1
    - **User Instructions**:
        1.  `pip install djangorestframework djangorestframework-simplejwt drf-spectacular`
        2.  `pip freeze > requirements.txt`
        3.  Update `settings.py` as described. Example `REST_FRAMEWORK` config:
            ```python
            REST_FRAMEWORK = {
                'DEFAULT_AUTHENTICATION_CLASSES': (
                    'rest_framework_simplejwt.authentication.JWTAuthentication',
                ),
                'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
                # Add other configurations like permissions later
            }
            SPECTACULAR_SETTINGS = {
                'TITLE': 'Simple Note Taking App API',
                'DESCRIPTION': 'API for the Simple Note Taking App',
                'VERSION': '1.0.0',
                'SERVE_INCLUDE_SCHEMA': False, # Schema available via /api/schema/
            }
            ```

- [ ] Step 10: Setup API Root and drf-spectacular URLs
    - **Task**: Create a root `api/` URL namespace. Add `drf-spectacular` URLs for Swagger UI and schema download.
    - **Files**:
        - `notely_project/notely_project/urls.py`: Include `api.urls` (to be created) and `drf_spectacular` URLs.
        - `notely_project/api/urls.py`: Create this file for API specific URL patterns.
    - **Step Dependencies**: Step 9
    - **User Instructions**:
        In `notely_project/urls.py`:
        ```python
        from django.contrib import admin # Ensure admin is imported
        from django.urls import path, include
        from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api/', include('api.urls')), # To be created
            path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
            path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]
        ```
        Create an empty `api/urls.py` for now.

- [ ] Step 11: Implement User Serializer and Registration/View (Basic)
    - **Task**: Create a `UserSerializer` for the `CustomUser` model (excluding sensitive fields like `password_hash` for general GET, but including `email`, `role`). Potentially a `UserRegistrationSerializer` if needed later, but admin creation is primary.
    - **Files**:
        - `notely_project/users/serializers.py`: Create `UserSerializer`.
    - **Step Dependencies**: Step 5, Step 9

- [ ] Step 12: Implement JWT Token Obtain, Refresh, and Blacklist Endpoints
    - **Task**: Configure URL patterns for `TokenObtainPairView`, `TokenRefreshView` from `rest_framework_simplejwt`. Implement token blacklisting for logout.
    - **Files**:
        - `notely_project/api/urls.py`: Add JWT token URLs.
        - `notely_project/users/views.py`: Create a custom view for logout that handles blacklisting.
        - `notely_project/notely_project/settings.py`: Add `rest_framework_simplejwt.token_blacklist` to `INSTALLED_APPS`. Configure `SIMPLE_JWT` settings (e.g., token lifetimes).
    - **Step Dependencies**: Step 9, Step 5
    - **User Instructions**:
        1.  Update `settings.py` to include `rest_framework_simplejwt.token_blacklist` and configure `SIMPLE_JWT` (access token lifetime, refresh token lifetime, blacklist after rotation). Add `from datetime import timedelta` at the top of `settings.py`.
            ```python
            # At the top of settings.py
            from datetime import timedelta

            # ... other settings ...

            INSTALLED_APPS = [
                # ...
                'rest_framework_simplejwt.token_blacklist',
                # ...
            ]

            SIMPLE_JWT = {
                'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
                'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
                'ROTATE_REFRESH_TOKENS': True,
                'BLACKLIST_AFTER_ROTATION': True,
                'UPDATE_LAST_LOGIN': True, # For tracking active users
                # ... other settings
            }
            ```
        2.  Add URLs to `api/urls.py`:
            ```python
            # api/urls.py
            from django.urls import path
            from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
            from users.views import LogoutView # To be created

            urlpatterns = [
                path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('logout/', LogoutView.as_view(), name='auth_logout'),
            ]
            ```
        3. Run `python manage.py migrate` (due to `token_blacklist` app).
        4. Create `LogoutView` in `users/views.py`:
            ```python
            # users/views.py
            from rest_framework.views import APIView
            from rest_framework.response import Response
            from rest_framework import status
            from rest_framework_simplejwt.tokens import RefreshToken
            from rest_framework.permissions import IsAuthenticated

            class LogoutView(APIView):
                permission_classes = (IsAuthenticated,)

                def post(self, request):
                    try:
                        refresh_token = request.data["refresh"]
                        token = RefreshToken(refresh_token)
                        token.blacklist()
                        return Response(status=status.HTTP_205_RESET_CONTENT)
                    except Exception as e:
                        # Consider logging the exception e
                        return Response({"detail": "Invalid refresh token or an error occurred."}, status=status.HTTP_400_BAD_REQUEST)
            ```


## Phase 3: Backend - Note Management API (Regular User)

- [ ] Step 13: Create Note Serializer
    - **Task**: Create a `NoteSerializer` for the `Note` model. Ensure it handles `user_id` appropriately (e.g., read-only, set to current user on create). Include `title`, `content`, `created_at`, `updated_at`.
    - **Files**:
        - `notely_project/notes_app/serializers.py`: Define `NoteSerializer`.
    - **Step Dependencies**: Step 6, Step 9

- [ ] Step 14: Implement Note List and Create API Views (User-Specific)
    - **Task**: Create a `ViewSet` or `APIView` for notes. Implement `list` (own notes only) and `create` actions. Set the note's user to the currently authenticated user upon creation. Add `IsAuthenticated` permission.
    - **Files**:
        - `notely_project/notes_app/views.py`: Create `NoteViewSet`.
        - `notely_project/api/urls.py`: Register `NoteViewSet` URLs.
        - `notely_project/notes_app/permissions.py`: Create `IsOwner` permission (for update/delete later).
    - **Step Dependencies**: Step 13
    - **User Instructions**:
        In `notes_app/views.py`:
        ```python
        from rest_framework import viewsets, permissions
        from .models import Note
        from .serializers import NoteSerializer
        # from .permissions import IsOwner # To be created in next step

        class NoteViewSet(viewsets.ModelViewSet):
            serializer_class = NoteSerializer
            permission_classes = [permissions.IsAuthenticated] 

            def get_queryset(self):
                # Ensure users only see their own notes, ordered by creation date descending
                return Note.objects.filter(user=self.request.user).order_by('-created_at')

            def perform_create(self, serializer):
                serializer.save(user=self.request.user)
        ```
        In `api/urls.py`, extend urlpatterns with a router for notes:
        ```python
        # api/urls.py
        # ... other imports (path, TokenObtainPairView, etc.)
        from rest_framework.routers import DefaultRouter
        from notes_app.views import NoteViewSet

        router = DefaultRouter()
        router.register(r'notes', NoteViewSet, basename='note')

        urlpatterns = [
            path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('logout/', LogoutView.as_view(), name='auth_logout'),
            # ... other non-router paths
        ] + router.urls # Add router URLs to the existing urlpatterns
        ```

- [ ] Step 15: Implement Note Retrieve, Update, Delete API Views (User-Specific)
    - **Task**: Implement `retrieve`, `update`, `partial_update`, and `destroy` actions in `NoteViewSet`. Ensure users can only operate on their own notes using a custom `IsOwner` permission.
    - **Files**:
        - `notely_project/notes_app/views.py`: Update `NoteViewSet` permissions.
        - `notely_project/notes_app/permissions.py`: Define `IsOwner` permission.
    - **Step Dependencies**: Step 14
    - **User Instructions**:
        Create `notes_app/permissions.py`:
        ```python
        from rest_framework import permissions

        class IsOwner(permissions.BasePermission):
            """
            Custom permission to only allow owners of an object to edit or view it.
            """
            def has_object_permission(self, request, view, obj):
                # Read permissions are allowed to any request,
                # so we'll always allow GET, HEAD or OPTIONS requests.
                # if request.method in permissions.SAFE_METHODS:
                #     return True # This would allow any authenticated user to read, which is not desired for notes.

                # Instance must have an attribute named `user`.
                return obj.user == request.user
        ```
        In `notes_app/views.py`, update `NoteViewSet`:
        ```python
        # ... imports
        from .permissions import IsOwner

        class NoteViewSet(viewsets.ModelViewSet):
            serializer_class = NoteSerializer
            # permission_classes = [permissions.IsAuthenticated, IsOwner] # Applied generally

            def get_queryset(self):
                return Note.objects.filter(user=self.request.user).order_by('-created_at')

            def perform_create(self, serializer):
                serializer.save(user=self.request.user)

            def get_permissions(self):
                """
                Instantiates and returns the list of permissions that this view requires.
                """
                if self.action == 'list' or self.action == 'create':
                    permission_classes = [permissions.IsAuthenticated]
                else: # 'retrieve', 'update', 'partial_update', 'destroy'
                    permission_classes = [permissions.IsAuthenticated, IsOwner]
                return [permission() for permission in permission_classes]
        ```

- [ ] Step 16: Implement Note Sorting and Searching API
    - **Task**: Add sorting (`title`, `created_at`) and searching (`title` using `icontains`) to the `NoteViewSet` list action. Use DRF's built-in `OrderingFilter` and `SearchFilter`.
    - **Files**:
        - `notely_project/notes_app/views.py`: Modify `NoteViewSet` to include filter backends.
        - `notely_project/requirements.txt`: (Ensure `django-filter` is added if more complex filtering is needed, but for now, DRF defaults are fine).
        - `notely_project/notely_project/settings.py`: (Ensure `django_filters` is in `INSTALLED_APPS` if used and `DEFAULT_FILTER_BACKENDS` is configured in `REST_FRAMEWORK` if `django-filter` is chosen over DRF's built-ins for more complex cases). For this step, DRF's built-in `SearchFilter` and `OrderingFilter` are sufficient.
    - **Step Dependencies**: Step 14
    - **User Instructions**:
        Update `notes_app/views.py`:
        ```python
        from rest_framework.filters import OrderingFilter, SearchFilter
        # ... other imports from notes_app.views

        class NoteViewSet(viewsets.ModelViewSet):
            serializer_class = NoteSerializer
            # get_permissions, get_queryset, perform_create as before

            filter_backends = [SearchFilter, OrderingFilter]
            search_fields = ['title'] # For ?search=term (LIKE query on title, case-insensitive by default for icontains)
            ordering_fields = ['title', 'created_at'] # For ?ordering=title or ?ordering=-created_at
                                                    # Default ordering is handled in get_queryset if no param.
        ```
        If `django-filter` was intended for simple search, using `SearchFilter` is more straightforward. `django-filter` is powerful for field-based filtering. The spec said `LIKE` which `SearchFilter` with `search_fields` provides.

## Phase 4: Frontend - Basic Structure, Layout, and API Client Setup

- [ ] Step 17: Setup Basic React Router
    - **Task**: Install `react-router-dom`. Create basic routes for Login, Notes Dashboard, and potentially a Home page.
    - **Files**:
        - `notely_frontend/package.json`: Add `react-router-dom`.
        - `notely_frontend/src/main.tsx`: Wrap `App` with `BrowserRouter`.
        - `notely_frontend/src/App.tsx`: Define routes.
        - `notely_frontend/src/pages/LoginPage.tsx`: Create placeholder.
        - `notely_frontend/src/pages/NotesDashboardPage.tsx`: Create placeholder.
        - `notely_frontend/src/pages/HomePage.tsx`: Create placeholder.
    - **Step Dependencies**: Step 3
    - **User Instructions**:
        1.  `cd notely_frontend`
        2.  `npm install react-router-dom`

- [ ] Step 18: Create Main Layout Components
    - **Task**: Create a `Navbar` component. Create a `MainLayout` component that includes the `Navbar` and an outlet for page content. Apply basic Tailwind styling.
    - **Files**:
        - `notely_frontend/src/components/Navbar.tsx`
        - `notely_frontend/src/components/layouts/MainLayout.tsx`
        - `notely_frontend/src/App.tsx`: Use `MainLayout` for relevant routes.
    - **Step Dependencies**: Step 4, Step 17

- [ ] Step 19: Setup API Client (Axios) and Environment Configuration
    - **Task**: Install `axios`. Create an Axios instance configured with `baseURL` for the API (e.g., `http://localhost:8000/api`). Use Vite environment variables for the API base URL.
    - **Files**:
        - `notely_frontend/package.json`: Add `axios`.
        - `notely_frontend/src/services/apiClient.ts`: Create Axios instance.
        - `notely_frontend/.env.development`: Define `VITE_API_BASE_URL=http://localhost:8000/api`.
        - `notely_frontend/src/vite-env.d.ts`: Add type definition for `VITE_API_BASE_URL`.
    - **Step Dependencies**: Step 3
    - **User Instructions**:
        1.  `cd notely_frontend`
        2.  `npm install axios`
        3.  Create `.env.development` with `VITE_API_BASE_URL=http://localhost:8000/api`.
        4.  Update `src/vite-env.d.ts` to include:
            ```typescript
            /// <reference types="vite/client" />

            interface ImportMetaEnv {
              readonly VITE_API_BASE_URL: string;
              // more env variables...
            }

            interface ImportMeta {
              readonly env: ImportMetaEnv;
            }
            ```

- [ ] Step 20: Setup OpenAPI TypeScript Codegen
    - **Task**: Install `openapi-typescript-codegen`. Add a script to `package.json` to generate an Axios API client from the backend's OpenAPI schema.
    - **Files**:
        - `notely_frontend/package.json`: Add dev dependency and script.
        - `notely_frontend/src/services/apiClientGenerated/` (or similar): Placeholder for generated code (will be created by the tool).
    - **Step Dependencies**: Step 10 (Backend API schema URL), Step 19
    - **User Instructions**:
        1.  `cd notely_frontend`
        2.  `npm install -D openapi-typescript-codegen`
        3.  Add a script to `package.json`'s `"scripts"` section:
            `"generate-api": "openapi-typescript-codegen --input http://localhost:8000/api/schema/?format=openapi --output ./src/services/apiClientGenerated --client axios --useOptions"`
        4.  Run the script `npm run generate-api` to perform an initial generation once the backend API schema is available and serving. (Ensure backend is running).
        5.  The generated client can then be imported and used instead of manually crafting all `axios` calls.

- [ ] Step 21: Basic Authentication Context/Store
    - **Task**: Create a simple React Context for managing authentication state (token, user info, `isAuthenticated` status).
    - **Files**:
        - `notely_frontend/src/contexts/AuthContext.tsx`.
        - `notely_frontend/src/App.tsx`: Wrap app with AuthProvider.
        - `notely_frontend/src/types/user.ts`: (Optional) Define user type.
    - **Step Dependencies**: Step 3
    - **User Instructions**: (If using Zustand instead, `npm install zustand` and create a store file e.g. `src/stores/authStore.ts`)

## Phase 5: Frontend - User Authentication

- [ ] Step 22: Implement Login Page UI
    - **Task**: Create the UI for the login page with email and password fields, and a submit button. Use Tailwind CSS for styling.
    - **Files**:
        - `notely_frontend/src/pages/LoginPage.tsx`: Implement form UI.
        - `notely_frontend/src/components/forms/LoginForm.tsx` (Optional, if abstracting the form).
    - **Step Dependencies**: Step 4, Step 17

- [ ] Step 23: Implement Login Logic
    - **Task**: Handle form submission on `LoginPage.tsx`. Call the backend login API endpoint (`/token/`) using the generated API client or Axios instance. On success, store JWT (access and refresh tokens) in `localStorage` and update the AuthContext. Redirect to the notes dashboard. Handle login errors and display messages.
    - **Files**:
        - `notely_frontend/src/pages/LoginPage.tsx`: Add login logic.
        - `notely_frontend/src/contexts/AuthContext.tsx`: Add login function to update context and store tokens.
        - `notely_frontend/src/services/apiClient.ts` (or the generated client): Ensure it can have tokens attached for subsequent requests.
    - **Step Dependencies**: Step 12 (Backend Auth API), Step 19 (or 20), Step 21, Step 22

- [ ] Step 24: Create Protected Route Component
    - **Task**: Create a `ProtectedRoute` component that checks if the user is authenticated (via AuthContext). If not, redirect to the login page.
    - **Files**:
        - `notely_frontend/src/components/routes/ProtectedRoute.tsx`
        - `notely_frontend/src/App.tsx`: Use `ProtectedRoute` for routes like Notes Dashboard.
    - **Step Dependencies**: Step 17, Step 21

- [ ] Step 25: Implement Logout Functionality
    - **Task**: Add a logout button (e.g., in `Navbar`). On click, call the backend logout API (Step 12, `/logout/`), clear tokens from `localStorage`, update AuthContext, and redirect to the login page.
    - **Files**:
        - `notely_frontend/src/components/Navbar.tsx`: Add logout button and logic.
        - `notely_frontend/src/contexts/AuthContext.tsx`: Add logout function to update context and clear tokens.
    - **Step Dependencies**: Step 12 (Backend Logout API), Step 18, Step 23

- [ ] Step 26: Implement Automatic JWT Token Renewal
    - **Task**: If using a manually configured Axios instance (from Step 19), set up an Axios interceptor to handle 401 errors. If a 401 is due to an expired access token, use the refresh token to request a new access token from `/token/refresh/`. Update stored tokens and retry the original request. If refresh fails, log out the user. If using `openapi-typescript-codegen` (Step 20), this might require custom configuration or wrapping the generated client.
    - **Files**:
        - `notely_frontend/src/services/apiClient.ts` (if manual Axios): Add Axios response interceptor.
        - `notely_frontend/src/contexts/AuthContext.tsx`: May need to expose refresh token or handle logout on refresh failure.
    - **Step Dependencies**: Step 12 (Backend Refresh API), Step 19 (or 20), Step 23

- [ ] Step 27: Setup Toast Notifications
    - **Task**: Install and configure a toast notification library (e.g., `react-toastify` or `sonner`). Use it for login success/error, logout, and other important messages.
    - **Files**:
        - `notely_frontend/package.json`: Add toast library.
        - `notely_frontend/src/App.tsx`: Initialize toast container.
        - `notely_frontend/src/pages/LoginPage.tsx`: Use toasts for feedback.
    - **Step Dependencies**: Step 3
    - **User Instructions**: `npm install react-toastify` (or chosen library like `sonner`).

## Phase 6: Frontend - Note Management (Regular User)

- [ ] Step 28: Notes Dashboard Page - List Notes
    - **Task**: Create the UI to display a list of the authenticated user's notes on `NotesDashboardPage.tsx`. Fetch notes using the API client (generated or manual). Display title, creation/update date. Handle loading and empty states.
    - **Files**:
        - `notely_frontend/src/pages/NotesDashboardPage.tsx`
        - `notely_frontend/src/components/notes/NoteListItem.tsx`
        - `notely_frontend/src/services/apiClientGenerated/services/...` (or manual service file)
    - **Step Dependencies**: Step 14 (Backend API), Step 20 (API Client), Step 24 (Protected Route), Step 27 (Toasts)

- [ ] Step 29: Implement Note Sorting UI
    - **Task**: Add UI elements (e.g., dropdown) on the `NotesDashboardPage.tsx` to allow sorting notes by `title` and `created_at` (asc/desc). Pass sorting parameters to the API.
    - **Files**:
        - `notely_frontend/src/pages/NotesDashboardPage.tsx`: Add sorting controls and logic.
    - **Step Dependencies**: Step 16 (Backend Sorting API), Step 28

- [ ] Step 30: Implement Note Search UI
    - **Task**: Add a search input field on `NotesDashboardPage.tsx` to filter notes by title. Call the API with the search term.
    - **Files**:
        - `notely_frontend/src/pages/NotesDashboardPage.tsx`: Add search input and logic.
    - **Step Dependencies**: Step 16 (Backend Search API), Step 28

- [ ] Step 31: Create Note Page - Form and Logic
    - **Task**: Create a new page/route for creating a note. Implement a form with `title` and `content` (plain text) fields. On submit, call the create note API endpoint. Redirect or update list on success. Implement form validation and feedback.
    - **Files**:
        - `notely_frontend/src/pages/CreateNotePage.tsx`
        - `notely_frontend/src/components/notes/NoteForm.tsx`
        - `notely_frontend/src/App.tsx`: Add route for create note page.
    - **Step Dependencies**: Step 14 (Backend API), Step 27 (Toasts), Step 20 (API Client)

- [ ] Step 32: View Single Note Page
    - **Task**: Create a page/route to view a single note's details (`title` and `content`). Fetch the specific note by ID.
    - **Files**:
        - `notely_frontend/src/pages/ViewNotePage.tsx`
        - `notely_frontend/src/App.tsx`: Add route for view note page (e.g., `/notes/:id`).
    - **Step Dependencies**: Step 15 (Backend API), Step 28 (to link from list), Step 20 (API Client)

- [ ] Step 33: Update Note Page - Form and Logic
    - **Task**: Create a page/route for editing an existing note. Pre-fill the form with the note's current `title` and `content`. On submit, call the update note API endpoint. Implement form validation and feedback.
    - **Files**:
        - `notely_frontend/src/pages/EditNotePage.tsx`
        - `notely_frontend/src/components/notes/NoteForm.tsx`: Reuse or adapt.
        - `notely_frontend/src/App.tsx`: Add route for edit note page (e.g., `/notes/:id/edit`).
    - **Step Dependencies**: Step 15 (Backend API), Step 32 (to link from view/list), Step 20 (API Client)

- [ ] Step 34: Implement Delete Note Functionality
    - **Task**: Add a delete button to the note list items or view note page. Implement a confirmation dialog before deleting. Call the delete note API endpoint. Update UI on success.
    - **Files**:
        - `notely_frontend/src/pages/NotesDashboardPage.tsx` (or `NoteListItem.tsx`)
        - `notely_frontend/src/pages/ViewNotePage.tsx`
        - `notely_frontend/src/components/common/ConfirmationModal.tsx`
    - **Step Dependencies**: Step 15 (Backend API), Step 28, Step 32, Step 20 (API Client)

- [ ] Step 35: Implement Loading States for Async Operations
    - **Task**: Ensure all asynchronous operations (fetching, creating, updating, deleting notes; login/logout) display clear loading indicators (e.g., spinners, disabled buttons).
    - **Files**: Affects multiple components and pages involved in async calls.
        - `notely_frontend/src/pages/LoginPage.tsx`
        - `notely_frontend/src/pages/NotesDashboardPage.tsx`
        - `notely_frontend/src/pages/CreateNotePage.tsx`, `EditNotePage.tsx`
        - `notely_frontend/src/components/notes/NoteForm.tsx`
    - **Step Dependencies**: Previous frontend steps involving API calls.

- [ ] Step 36: Implement Frontend Form Validation and Error Display
    - **Task**: Implement real-time validation feedback for forms (login, note creation/editing) using a library like `react-hook-form` or manual state management. Display errors from API responses clearly (e.g., using toast notifications or inline messages).
    - **Files**: Affects form components.
        - `notely_frontend/src/pages/LoginPage.tsx` (or `LoginForm.tsx`)
        - `notely_frontend/src/components/notes/NoteForm.tsx`
    - **Step Dependencies**: Previous frontend steps with forms.
    - **User Instructions**: (Optional, but recommended) `npm install react-hook-form`.

## Phase 7: Backend - Administrator Capabilities

- [ ] Step 37: Create User Management API Endpoints (Admin)
    - **Task**: Implement API endpoints for administrators to manage users:
        - List all users (`GET /api/admin/users/`)
        - Retrieve a specific user's details (`GET /api/admin/users/{id}/`)
        - Update a user's details (role, `is_active`) (`PUT/PATCH /api/admin/users/{id}/`)
    - Create an `AdminUserSerializer` for these operations. Ensure `IsAdmin` permission.
    - **Files**:
        - `notely_project/users/serializers.py`: Add `AdminUserSerializer`.
        - `notely_project/users/views.py`: Create `AdminUserViewSet`.
        - `notely_project/api/urls.py`: Add URLs for admin user management under an `admin/` prefix to the router.
        - `notely_project/users/permissions.py`: Define `IsAdmin` permission.
    - **Step Dependencies**: Step 5, Step 9, Step 11
    - **User Instructions**:
        Define `IsAdmin` in `users/permissions.py`:
        ```python
        # users/permissions.py
        # from rest_framework import permissions # already imported if IsOwner exists

        class IsAdmin(permissions.BasePermission):
            def has_permission(self, request, view):
                return request.user and request.user.is_authenticated and request.user.role == 'admin'
        ```
        Register `AdminUserViewSet` in `api/urls.py` within the existing router or a new admin-specific router:
        ```python
        # api/urls.py
        # from users.views import AdminUserViewSet
        # router.register(r'admin/users', AdminUserViewSet, basename='admin-user')
        # urlpatterns will be automatically updated
        ```

- [ ] Step 38: Implement Admin Password Reset API Endpoint
    - **Task**: Create an API endpoint for administrators to set a temporary password for a user (`POST /api/admin/users/{id}/reset-password/`). Admin provides the new password. The user's `set_password` method should be used.
    - **Files**:
        - `notely_project/users/views.py`: Add custom action to `AdminUserViewSet`.
        - `notely_project/users/serializers.py`: Add `AdminPasswordResetSerializer`.
        - `notely_project/api/urls.py`: (Handled by ViewSet custom action if done that way).
    - **Step Dependencies**: Step 37

- [ ] Step 39: Implement Admin Full CRUD on All Notes API Endpoints
    - **Task**: Create API endpoints for administrators to perform CRUD operations on any note in the system. This involves a new ViewSet (`AdminNoteViewSet`) that does not filter by user.
        - List all notes (`GET /api/admin/notes/`)
        - Retrieve any note (`GET /api/admin/notes/{id}/`)
        - Update any note (`PUT/PATCH /api/admin/notes/{id}/`)
        - Delete any note (`DELETE /api/admin/notes/{id}/`)
    - Use `NoteSerializer` or create `AdminNoteSerializer` if different. Ensure `IsAdmin` permission.
    - **Files**:
        - `notely_project/notes_app/serializers.py`: (Use existing `NoteSerializer` or create `AdminNoteSerializer`).
        - `notely_project/notes_app/views.py`: Create `AdminNoteViewSet`.
        - `notely_project/api/urls.py`: Register `AdminNoteViewSet` with the router under an `admin/` prefix.
    - **Step Dependencies**: Step 6, Step 9, Step 13, Step 37 (for IsAdmin permission)

- [ ] Step 40: Implement System Statistics API Endpoint (Admin)
    - **Task**: Create an API endpoint (`GET /api/admin/statistics/`) that returns:
        - Total users
        - Total notes
        - Notes per user (average)
        - Active users in the last 7 days (users who have `last_login` within the last 7 days).
    - Ensure `IsAdmin` permission.
    - **Files**:
        - `notely_project/api/views.py` (or a new `admin_dashboard/views.py`): Create `SystemStatisticsView`.
        - `notely_project/api/urls.py`: Add URL for this view.
    - **Step Dependencies**: Step 5, Step 6, Step 12 (for `UPDATE_LAST_LOGIN`), Step 37

- [ ] Step 41: Implement User Login Log API Endpoint (Admin)
    - **Task**: Log user login events. For simplicity, this might just rely on `CustomUser.last_login`. Create an API endpoint (`GET /api/admin/logs/logins/`) to list users with their last login time, ordered by most recent. A more detailed log would require a `LoginLog` model and signal handlers. PRD: "User logins (details of other logs like admin actions, failed logins to be decided later if necessary)". We'll use `User.last_login` for now for "active users" and "login logs" display.
    - **Files**:
        - `notely_project/users/serializers.py`: Potentially a `UserLoginInfoSerializer`.
        - `notely_project/api/views.py` (or `admin_dashboard/views.py`): Create `UserLoginLogView`.
        - `notely_project/api/urls.py`: Add URL.
    - **Step Dependencies**: Step 5, Step 37
    - **User Instructions**: The `UserLoginLogView` would query `CustomUser` objects, focusing on `email` and `last_login`, and ordering by `last_login`.

## Phase 8: Frontend - Administrator Dashboard

- [ ] Step 42: Create Admin Dashboard Layout and Protected Routes
    - **Task**: Create a specific layout for the admin section. Implement protected routes for admin pages, checking for `user.role === 'admin'` from AuthContext.
    - **Files**:
        - `notely_frontend/src/components/layouts/AdminLayout.tsx`
        - `notely_frontend/src/App.tsx`: Add admin routes using `AdminLayout` and a new `AdminProtectedRoute` component.
        - `notely_frontend/src/components/routes/AdminProtectedRoute.tsx`
        - `notely_frontend/src/contexts/AuthContext.tsx`: Ensure user (with role) is available.
    - **Step Dependencies**: Step 18, Step 24 (concept for protected route), Step 21 (AuthContext)

- [ ] Step 43: Admin - User Management UI (List, View Details)
    - **Task**: Implement UI for listing users and viewing their details (email, role, status `is_active`). Fetch data from admin user management API.
    - **Files**:
        - `notely_frontend/src/pages/admin/UserListPage.tsx`
        - `notely_frontend/src/pages/admin/UserDetailsPage.tsx` (can be a modal or separate page)
    - **Step Dependencies**: Step 37 (Backend API), Step 20 (API Client), Step 42

- [ ] Step 44: Admin - User Management UI (Actions: Role Change, Disable/Enable, Password Reset)
    - **Task**: Add UI elements (buttons, forms/modals) to change user roles, disable/enable accounts, and reset passwords. Integrate with respective backend APIs.
    - **Files**:
        - `notely_frontend/src/pages/admin/UserListPage.tsx` (for actions on list items)
        - `notely_frontend/src/pages/admin/UserDetailsPage.tsx` (if using a detail page for actions)
        - `notely_frontend/src/components/admin/UserActions.tsx` (example component)
    - **Step Dependencies**: Step 37, Step 38 (Backend APIs), Step 43

- [ ] Step 45: Admin - All Notes View UI (CRUD)
    - **Task**: Implement UI for administrators to view, search, sort, and perform CRUD operations (view, update, delete - creation by admin might be less common but possible) on all notes from all users.
    - **Files**:
        - `notely_frontend/src/pages/admin/AdminAllNotesPage.tsx`
    - **Step Dependencies**: Step 39 (Backend API), Step 20 (API Client), Step 42

- [ ] Step 46: Admin - System Statistics Display UI
    - **Task**: Implement UI to display system statistics (total users, total notes, etc.) fetched from the backend.
    - **Files**:
        - `notely_frontend/src/pages/admin/AdminStatisticsPage.tsx`
    - **Step Dependencies**: Step 40 (Backend API), Step 20 (API Client), Step 42

- [ ] Step 47: Admin - System Logs (User Logins) Display UI
    - **Task**: Implement UI to display user login information (e.g., list of users with their last login times) fetched from the backend.
    - **Files**:
        - `notely_frontend/src/pages/admin/AdminLoginLogsPage.tsx`
    - **Step Dependencies**: Step 41 (Backend API), Step 20 (API Client), Step 42

## Phase 9: Backend - API Security & Final Touches

- [ ] Step 48: Implement Rate Limiting
    - **Task**: Configure rate limiting for sensitive endpoints like login, using `django-ratelimit`.
    - **Files**:
        - `notely_project/requirements.txt`: Add `django-ratelimit`.
        - `notely_project/notely_project/settings.py`: Configure `django-ratelimit` (e.g., `RATELIMIT_MIDDLEWARE`, default rates).
        - `notely_project/api/urls.py` (or `users/views.py`): Apply ratelimit decorators (e.g., `@ratelimit`) to specific views like `TokenObtainPairView`.
    - **Step Dependencies**: Step 12
    - **User Instructions**:
        1. `pip install django-ratelimit` and add to `requirements.txt`.
        2. Add `django_ratelimit` to `INSTALLED_APPS`.
        3. Add `RATELIMIT_MIDDLEWARE = 'django_ratelimit.middleware.RatelimitMiddleware'` to `MIDDLEWARE` (usually near the top).
        4. Configure default rates in `settings.py` or decorate views. Example for `TokenObtainPairView`:
           ```python
           # users/views.py or where TokenObtainPairView is extended/used
           # from ratelimit.decorators import ratelimit
           # from django.utils.decorators import method_decorator
           # @method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='post')
           # class DecoratedTokenObtainPairView(TokenObtainPairView): pass
           # Then use DecoratedTokenObtainPairView in urls.py
           ```
           Alternatively, configure via `RATELIMIT_VIEW` setting.

- [ ] Step 49: Configure CORS for Azure SWA Origin
    - **Task**: Install and configure `django-cors-headers` to allow requests specifically from the Azure Static Web Apps frontend origin (and localhost for dev). Use environment variables for allowed origins in production.
    - **Files**:
        - `notely_project/requirements.txt`: Add `django-cors-headers`.
        - `notely_project/notely_project/settings.py`: Add `corsheaders` to `INSTALLED_APPS` and `corsheaders.middleware.CorsMiddleware` to `MIDDLEWARE` (usually before `CommonMiddleware`). Configure `CORS_ALLOWED_ORIGINS` (preferred) or `CORS_ORIGIN_WHITELIST`.
    - **Step Dependencies**: Step 1
    - **User Instructions**:
        1. `pip install django-cors-headers` and add to `requirements.txt`.
        2. Update `settings.py` (add to `INSTALLED_APPS`, `MIDDLEWARE`).
           Example `MIDDLEWARE` order:
           ```python
           MIDDLEWARE = [
               'corsheaders.middleware.CorsMiddleware',
               # ... other middleware like SecurityMiddleware, WhiteNoiseMiddleware
               'django.middleware.common.CommonMiddleware',
               # ...
           ]
           ```
           Configure `CORS_ALLOWED_ORIGINS` (e.g., `['http://localhost:5173', 'https://your-swa-domain.azurestaticapps.net']`). Use environment variables for production origins.

- [ ] Step 50: Implement Global Error Handling Middleware for API
    - **Task**: Create a custom Django exception handler for DRF to ensure consistent JSON error responses for various exceptions (4xx, 5xx), including a `status_code` in the response body if not already present.
    - **Files**:
        - `notely_project/api/exception_handler.py`: Define custom handler.
        - `notely_project/notely_project/settings.py`: Configure `REST_FRAMEWORK` to use this handler via `EXCEPTION_HANDLER`.
    - **Step Dependencies**: Step 9
    - **User Instructions**:
        In `notely_project/notely_project/settings.py` update `REST_FRAMEWORK`:
        ```python
        REST_FRAMEWORK = {
            # ... other settings
            'EXCEPTION_HANDLER': 'api.exception_handler.custom_api_exception_handler',
        }
        ```
        Create `notely_project/api/exception_handler.py`:
        ```python
        from rest_framework.views import exception_handler

        def custom_api_exception_handler(exc, context):
            # Call REST framework's default exception handler first,
            # to get the standard error response.
            response = exception_handler(exc, context)

            # Now add the HTTP status code to the response.
            if response is not None:
                if 'status_code' not in response.data:
                     response.data['status_code'] = response.status_code
                
                # You can customize the error response structure further here if needed.
                # For example, ensuring 'detail' is always present or standardizing error codes.
                if 'detail' not in response.data and 'non_field_errors' in response.data:
                    response.data['detail'] = response.data['non_field_errors']


            return response
        ```

## Phase 10: Frontend - Final Polish

- [ ] Step 51: Ensure Responsive Design Across All Pages
    - **Task**: Test and refine Tailwind CSS classes to ensure all pages and components are fully responsive on desktop, tablet, and mobile devices.
    - **Files**: All `.tsx` files with UI.
    - **Step Dependencies**: All frontend UI steps.

- [ ] Step 52: Comprehensive UI/UX Review and Refinement
    - **Task**: Review the entire application for UI consistency, intuitiveness, and overall user experience. Make necessary adjustments to layout, typography, spacing, and component interactions, ensuring a clean and intuitive UI.
    - **Files**: All `.tsx` files with UI.
    - **Step Dependencies**: All frontend UI steps.

## Phase 11: Deployment Preparation

- [ ] Step 53: Create Dockerfile for Django Backend
    - **Task**: Write a `Dockerfile` to containerize the Django application. Include steps for installing dependencies from `requirements.txt`, copying application code, and running the application with Gunicorn.
    - **Files**:
        - `notely_project/Dockerfile`
        - `notely_project/requirements.txt`: Ensure it's up to date, add `gunicorn`.
        - `notely_project/.dockerignore`: To exclude `venv`, `__pycache__`, etc.
        - (Optional) `notely_project/entrypoint.sh`: Script for DB migrations, collecting static (if using WhiteNoise), starting Gunicorn.
    - **Step Dependencies**: All backend steps.
    - **User Instructions**:
        1. `pip install gunicorn` and add `gunicorn` to `notely_project/requirements.txt`.
        2. Create `.dockerignore`.

- [ ] Step 54: Configure Django Settings for Production
    - **Task**: Update `settings.py` to use environment variables for `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and database connection string (e.g., `DATABASE_URL`). Configure static file serving for production using WhiteNoise if Django is serving static files directly in the container.
    - **Files**:
        - `notely_project/notely_project/settings.py`
        - `notely_project/requirements.txt`: Add `whitenoise`, `python-dotenv` (if not already for local dev, can be useful for prod env vars too).
    - **Step Dependencies**: All backend steps.
    - **User Instructions**:
        1. `pip install whitenoise` and add to `requirements.txt`.
        2. Configure WhiteNoise middleware in `settings.py` (usually after `SecurityMiddleware`).
           `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
        3. Ensure environment variables are planned for Azure Container Apps.

- [ ] Step 55: Prepare Frontend for Build and Deployment
    - **Task**: Ensure the Vite build process (`npm run build`) generates optimized static assets in the `dist` folder. Configure any necessary environment variables for production API URL (e.g., in `.env.production` for `VITE_API_BASE_URL`).
    - **Files**:
        - `notely_frontend/vite.config.ts`
        - `notely_frontend/.env.production`: Define `VITE_API_BASE_URL` for your deployed backend.
    - **Step Dependencies**: All frontend steps.
    - **User Instructions**: The `notely_frontend/dist` folder generated by `npm run build` will be deployed to Azure Static Web Apps.

- [ ] Step 56: Write Unit Tests for Backend Logic (Placeholder Reminder)
    - **Task**: Implement unit tests for critical backend logic: models, serializers, utility functions, permissions, and view logic.
    - **Files**:
        - `notely_project/users/tests/test_models.py`, `test_views.py`, etc.
        - `notely_project/notes_app/tests/test_models.py`, `test_views.py`, etc.
    - **Step Dependencies**: Relevant backend feature steps.
    - **User Instructions**: Run tests using `python manage.py test users notes_app`.

- [ ] Step 57: Write Component/Integration Tests for Frontend (Placeholder Reminder)
    - **Task**: Implement tests for key React components and user flows (e.g., login, note creation, admin actions). Use libraries like Vitest (comes with Vite) or Jest, and React Testing Library.
    - **Files**:
        - `notely_frontend/src/components/tests/LoginForm.test.tsx` (example)
        - `notely_frontend/src/pages/tests/NotesDashboardPage.test.tsx` (example)
    - **Step Dependencies**: Relevant frontend feature steps.
    - **User Instructions**: Run tests using `npm test` (or `npm run test:unit` if configured that way in `package.json`).

## Summary and Key Considerations

This plan provides a granular breakdown for developing the Simple Note Taking App. Key considerations during implementation:

1.  **Sequential Execution**: Steps are designed to be largely sequential. Pay attention to `Step Dependencies`.
2.  **Atomic Changes**: Each step aims for atomic changes. If a step becomes too large, it might need further breakdown.
3.  **User Instructions**: Follow `User Instructions` carefully, as they involve manual setup, package installations, or commands crucial for the step's success.
4.  **Environment Variables**: Consistently use environment variables for sensitive data and configurations, especially for database credentials, secret keys, and API URLs in production.
5.  **API First**: Backend APIs are generally developed before frontend integration. The OpenAPI schema (`drf-spectacular`) should be generated and can be used to create or validate the frontend API client (`openapi-typescript-codegen`).
6.  **Security**:
    * JWT handling (storage, refresh, blacklisting) is critical.
    * Permissions (user vs. admin) must be strictly enforced on all API endpoints.
    * Input validation and sanitization are essential (DRF serializers help significantly).
    * Regularly update dependencies to patch security vulnerabilities.
7.  **Error Handling**: Implement robust error handling on both backend (consistent API error responses) and frontend (user-friendly messages, toast notifications).
8.  **Testing**: While placeholder steps for tests are included, continuous testing (unit, integration) throughout the development process is highly recommended.
9.  **Azure Deployment**:
    * Backend: The Dockerized Django app will be deployed to Azure Container Apps. Ensure database connection strings and other Azure-specific configurations are handled via environment variables.
    * Frontend: The Vite/React build output (static files) will be deployed to Azure Static Web Apps. Configure SWA to proxy API requests to the Container App.
    * Database: Azure Database for PostgreSQL will host the data.
10. **User Experience**: Focus on a clean, intuitive, and responsive UI as specified. Tailwind CSS should be leveraged effectively. Loading states and feedback mechanisms (toasts) are important.