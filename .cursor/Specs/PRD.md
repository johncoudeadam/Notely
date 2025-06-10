# PRD: Simple Note Taking App

## 1. Product overview
### 1.1 Document title and version
- PRD: Simple Note Taking App
- Version: 1.0

### 1.2 Product summary
This document outlines the product requirements for the Simple Note Taking App, a secure, multi-user, web-based application. The primary purpose of this application is to provide regular users with a private and straightforward platform to create, manage, and retrieve plain text notes. It also equips administrators with the necessary tools for user management, oversight of all note data, and system monitoring.

The application will feature a backend built with Django and PostgreSQL, exposing a RESTful API documented with OpenAPI (Swagger). Authentication will be JWT-based, supporting token refresh. The frontend will be a responsive Vite/React/TypeScript application using Tailwind CSS. Key considerations include robust security practices for authentication and data handling, and a clean, intuitive user interface. Deployment is planned on Microsoft Azure.

## 2. Goals
### 2.1 Business goals
- Provide a secure, reliable, and maintainable note-taking solution.
- Enable efficient user lifecycle management and system oversight for administrators.
- Establish a foundational platform that can be potentially extended with new features in the future.
- Ensure data integrity and user privacy through robust security measures.

### 2.2 User goals
- Regular Users: To securely create, view, edit, delete, and search their personal notes with ease.
- Regular Users: To have a private space for their notes, accessible only to them and system administrators.
- Administrators: To efficiently manage user accounts, including creation, password resets, role changes, and anabling/disabling accounts.
- Administrators: To have oversight of all notes within the system for support or compliance purposes.
- Administrators: To monitor basic system statistics and user login activity.

### 2.3 Non-goals
- Rich text editing (e.g., Markdown, WYSIWYG) for notes; only plain text is supported.
- Note tagging functionality.
- Advanced note filtering options beyond searching by title and sorting.
- Public user registration or self-signup; users are provisioned by administrators.
- End-to-end encryption of note content (security relies on authentication, secure transport, and at-rest protections for the database).
- Complex collaboration features between users.
- Granular permission systems beyond 'regular user' and 'administrator' roles.
- Advanced logging capabilities beyond user logins (for version 1.0).
- Forced password change by users after an admin resets their password (for version 1.0).

## 3. User personas
### 3.1 Key user types
- Regular User
- Administrator

### 3.2 Basic persona details
- **Regular User (e.g., Alex)**: Alex is a professional who needs a simple, secure digital notebook to quickly jot down ideas, meeting minutes, and personal reminders. Alex values privacy, speed, and a clutter-free interface, accessing notes from a desktop or mobile browser.
- **Administrator (e.g., Morgan)**: Morgan is an IT administrator responsible for managing the application, ensuring its smooth operation, and supporting users. Morgan needs tools to create and manage user accounts, oversee system usage, and troubleshoot issues, including accessing user notes if required for administrative purposes.

### 3.3 Role-based access
- **Regular User**: Can create new notes, read/view their own notes, update their own notes, delete their own notes, and search within their own notes by title. Can log in and log out.
- **Administrator**: Has full CRUD (Create, Read, Update, Delete) operations on all users' notes. Can manage user accounts through a dashboard (create new users, view user details, manually reset user passwords, change user roles, disable/enable user accounts). Can view system statistics (total users, total notes, notes per user, active users) and basic system logs (user logins). Can log in and log out. The initial administrator account is created via a Django `createsuperuser` management command.

## 4. Functional requirements
- **User Authentication** (Priority: High)
  - Administrators create new users via the Django admin interface.
  - Users can log in using email and password.
  - JWT tokens are issued upon successful login.
  - JWT tokens are automatically refreshed.
  - Users can log out, invalidating their session/token.
  - Passwords are securely hashed and stored.
- **Note Management (Regular User)** (Priority: High)
  - Users can create new notes with a title and plain text content.
  - Users can view a list of their own notes.
  - Users can sort their notes by title and creation date.
  - Users can open and read the full content of their notes.
  - Users can update the title and content of their existing notes.
  - Users can delete their own notes.
  - Users can search their notes by title using a simple `LIKE` query.
- **Note Management (Administrator)** (Priority: High)
  - Administrators can view a list of all notes from all users.
  - Administrators can read, update, and delete any note in the system.
  - Administrators can create notes on behalf of users (though user creation is primary focus).
- **User Management (Administrator)** (Priority: High)
  - Administrators can access a user management dashboard.
  - Administrators can view a list of all users and their details (email, role, status).
  - Administrators can manually reset a user's password (setting a temporary password and notifying the user out-of-band).
  - Administrators can change a user's role (e.g., from regular to admin, though care should be taken).
  - Administrators can disable or enable user accounts (via an `is_active` flag).
- **System Monitoring (Administrator)** (Priority: Medium)
  - Administrators can view system statistics: total users, total notes, notes per user, active users in the last 7 days (active = logged in).
  - Administrators can view system logs for user login events.
- **API** (Priority: High)
  - A RESTful API is implemented for all application functionalities.
  - The API is specified using OpenAPI/Swagger (auto-generated via `drf-spectacular`).
- **API Security** (Priority: High)
  - Implement rate limiting on sensitive endpoints (e.g., login). Specifics to be defined later.
  - Configure CORS to allow requests from the frontend origin (Azure SWA).
  - Implement request validation middleware.
  - Implement global error handling middleware.

## 5. User experience
### 5.1. Entry points & first-time user flow
- **Login Page**: Primary entry point for all users.
- **First-time Regular User (provisioned by Admin)**:
    - User receives credentials from an Administrator.
    - User navigates to the login page.
    - User enters credentials and logs in successfully.
    - User lands on their notes dashboard, which might be empty or show a welcome message.
    - User can immediately see options to create a new note.
- **First-time Administrator (after `createsuperuser`)**:
    - Admin uses `createsuperuser` credentials to log in via the standard login page or Django admin.
    - Admin lands on their dashboard with access to user management, note oversight, and statistics.

### 5.2. Core experience
- **Regular User - Note Creation**:
    - User logs in.
    - User navigates to "Create Note" action.
    - User enters a title and content, then saves.
    - The new note appears in their list of notes.
    - Clear feedback (e.g., toast notification) confirms note creation.
- **Regular User - Note Viewing & Management**:
    - User logs in and views their list of notes.
    - Notes are sortable by title or creation date.
    - User clicks on a note to view its full content.
    - User can choose to edit or delete the viewed note.
    - Search bar allows filtering notes by title.
- **Administrator - User Management**:
    - Admin logs in.
    - Admin navigates to the User Management Dashboard.
    - Admin can view users, click on a user to see details, and perform actions like disable, reset password, or change role.
    - Clear feedback confirms administrative actions.
- **Administrator - Note Oversight**:
    - Admin logs in.
    - Admin navigates to the "All Notes" view.
    - Admin can browse, search, view, edit, or delete any note from any user.

### 5.3. Advanced features & edge cases
- **Token Expiration and Refresh**: Seamless JWT refresh without interrupting user flow. If refresh fails, user is gracefully logged out and prompted to log in again.
- **Concurrent Edits**: Not explicitly handled for V1.0 (last write wins). This is a simplification.
- **Large Number of Notes**: UI should handle pagination or virtual scrolling efficiently for users or admins with many notes.
- **Invalid Input/Errors**: Clear, user-friendly error messages (e.g., toast notifications, inline field errors) for API errors or validation failures. Loading states for asynchronous operations.
- **Disabled Account Login Attempt**: User receives a clear message indicating their account is disabled.

### 5.4. UI/UX highlights
- **Clean and Intuitive Interface**: Minimalist design, focusing on content and ease of use.
- **Responsive Design**: Fully usable across desktop, tablet, and mobile browsers, leveraging Tailwind CSS.
- **Real-time Validation Feedback**: Forms provide immediate feedback on input validity.
- **Loading States**: Visual cues indicate when the application is processing data.
- **Toast Notifications**: Used for non-intrusive feedback on actions (success, error, warnings).
- **Accessibility**: Strive for good accessibility standards (e.g., keyboard navigation, ARIA attributes where appropriate), although not a primary explicit focus for V1 MVP beyond standard web practices.

## 6. Narrative
Alex, a freelance consultant, needs a simple and secure way to keep track of project notes, client requirements, and quick ideas throughout the day, accessible from any device. Alex finds the "Simple Note Taking App" appealing because it's offered by their organization, ensuring a level of trust and security. After an administrator creates an account, Alex logs in and is greeted by a clean interface. Alex can quickly create new notes, search through existing ones by title, and organize thoughts without fuss. The plain text editor is perfect for distraction-free writing. Alex feels confident that the notes are private and securely stored, allowing focus on the content rather than complex features.

## 7. Success metrics
### 7.1. User-centric metrics
- Number of daily/monthly active regular users.
- Average number of notes created per active regular user.
- User session duration.
- Task completion rate for core actions (e.g., creating a note, searching for a note).
- Frontend error rate experienced by users.

### 7.2. Business metrics
- User retention rate (for organizations that track this).
- Administrator efficiency (e.g., time taken to provision a new user, qualitative feedback).
- System uptime and reliability.

### 7.3. Technical metrics
- API average response time.
- API error rate (server-side).
- Database performance (query execution times).
- Adherence to security best practices (measured via audits or vulnerability scans if conducted).

## 8. Technical considerations
### 8.1. Integration points
- **User Interface (Azure SWA)** to **Backend API (Azure Container Apps)**: Primary integration via RESTful API calls over HTTPS.
- **Backend API** to **PostgreSQL Database (Azure Database for PostgreSQL)**: Standard database connection.
- **(Future) Email Service**: If password reset emails were to be implemented (currently out of scope for V1.0 for admin reset flow).

### 8.2. Data storage & privacy
- User credentials (passwords) must be securely hashed using a strong algorithm (e.g., Argon2, PBKDF2 - Django handles this).
- Note content is stored as plain text in the PostgreSQL database. While not end-to-end encrypted, access is controlled via authentication and authorization.
- Regular database backups should be configured for Azure Database for PostgreSQL.
- All data in transit (browser to SWA, SWA to Container App, Container App to DB) should be encrypted using TLS/SSL.
- Adherence to general data privacy principles; specific compliance (e.g., GDPR) requirements should be reviewed if applicable to the target users/organization.

### 8.3. Scalability & performance
- Azure Container Apps and Azure Database for PostgreSQL offer scaling capabilities.
- Efficient database queries and indexing (especially on `Notes.user_id`, `Notes.title`, `Users.email`).
- Pagination for lists of notes and users to ensure performance with large datasets.
- Optimize frontend bundle size and loading times using Vite and code splitting.
- Backend (Django) should be configured for production use (e.g., Gunicorn).

### 8.4. Potential challenges
- Ensuring robust JWT lifecycle management, especially secure token storage on the client and timely refresh/invalidation.
- Securely handling the out-of-band notification of temporary passwords by admins.
- Initial setup and configuration of the Azure services (SWA, Container Apps, PostgreSQL, networking).
- Achieving a truly intuitive and clean UI that meets diverse user expectations with Tailwind CSS.
- Time zone handling for `created_at` and `updated_at` timestamps if users are in different time zones.

## 9. Milestones & sequencing
### 9.1. Project estimate
- Medium: 6-8 weeks (for an initial MVP with a small, focused team)

### 9.2. Team size & composition
- Small Team: 2-4 total people
  - 1 Product Manager/Lead (can be part-time or dual-role)
  - 1-2 Full-stack Engineers (Django/React)
  - 0.5 QA specialist (can be one of the engineers or dedicated part-time)
  - (Designer if custom design beyond Tailwind utility-first is needed, otherwise engineer-led UI)

### 9.3. Suggested phases
- **Phase 1**: Core Backend & User Authentication (2-3 weeks)
  - Key deliverables: Django project setup, PostgreSQL schema, User model, JWT authentication (login, logout, refresh), REST API endpoints for auth, basic CRUD for Notes (user-specific), `drf-spectacular` setup, initial Docker setup.
- **Phase 2**: Core Frontend & Basic Note Management (2-3 weeks)
  - Key deliverables: Vite/React project setup, TypeScript, Tailwind CSS integration, Login page, Note list view, Note creation/view/edit/delete forms for regular users, API client generation/integration, basic protected routes.
- **Phase 3**: Administrator Features & Polish (2 weeks)
  - Key deliverables: Admin dashboard UI, User management features (list users, disable/enable, reset password, change role), All notes view for admins, System statistics display, System logs view (user logins), UI/UX refinement, error handling, deployment to Azure.

## 10. User stories

### 10.1. Admin: Create Initial Admin User
- **ID**: US-001
- **Description**: As a System Deployer, I want to create an initial administrator account so that the system can be managed.
- **Acceptance criteria**:
  - The `createsuperuser` Django management command successfully creates a user with administrative privileges.
  - The created administrator can log in using the chosen credentials.

### 10.2. Admin: Create New Regular User
- **ID**: US-002
- **Description**: As an Administrator, I want to create a new regular user account via the Django admin interface so that a new individual can use the note-taking application.
- **Acceptance criteria**:
  - Admin can access a user creation form within the Django admin or a dedicated admin dashboard.
  - Admin can input user details (email, initial password, role='regular').
  - Upon submission, a new user account is created with the `is_active` flag set to true by default.
  - The new user's password is securely hashed and stored.
  - The new user appears in the list of users.

### 10.3. User: Login
- **ID**: US-003
- **Description**: As a User (Regular or Admin), I want to log in to the application using my email and password so that I can access my notes or administrative functions.
- **Acceptance criteria**:
  - A login form is available with fields for email and password.
  - Upon submitting correct credentials, a JWT access token and refresh token are returned.
  - User is redirected to their respective dashboard (notes list for regular users, admin panel for admins).
  - If credentials are incorrect, an appropriate error message is displayed.
  - Login attempts are rate-limited to prevent brute-force attacks.

### 10.4. User: Secure Session with JWT
- **ID**: US-004
- **Description**: As a logged-in User, I want my session to be securely managed using JWTs so that my access to the application is authorized and protected.
- **Acceptance criteria**:
  - JWT access tokens are sent with every authenticated API request.
  - Access tokens have a short expiry time.
  - Refresh tokens are used to obtain new access tokens automatically before the current one expires.
  - If access token is expired and refresh token is invalid/expired, user is logged out or prompted to re-login.
  - API endpoints correctly validate JWTs and enforce permissions based on user role.

### 10.5. User: Logout
- **ID**: US-005
- **Description**: As a logged-in User, I want to log out of the application so that my session is terminated securely.
- **Acceptance criteria**:
  - A logout button/option is available.
  - Clicking logout invalidates the JWT access token on the client-side (e.g., remove from storage).
  - Server-side blacklisting of the token is implemented to prevent reuse until expiry.
  - User is redirected to the login page.

### 10.6. Regular User: Create Note
- **ID**: US-006
- **Description**: As a Regular User, I want to create a new note with a title and content so that I can record information.
- **Acceptance criteria**:
  - An option to create a new note (e.g., a button or link) is available.
  - A form is provided to input a note title (mandatory) and content (plain text, mandatory).
  - Upon saving, the note is associated with the logged-in user.
  - The note includes `created_at` and `updated_at` timestamps.
  - The user receives feedback (e.g., toast notification) that the note was created successfully.
  - The new note appears in the user's list of notes.

### 10.7. Regular User: View Own Notes List
- **ID**: US-007
- **Description**: As a Regular User, I want to view a list of my own notes so that I can see all my recorded information.
- **Acceptance criteria**:
  - After login, the user is presented with a list of their notes.
  - Each note in the list displays at least its title and creation/update date.
  - Only notes created by the logged-in user are displayed.
  - If the user has no notes, a clear message or state indicates this.
  - The list is sortable by title (alphabetically) and `created_at` (chronologically, asc/desc).
  - Pagination or infinite scrolling is implemented if the number of notes is large.

### 10.8. Regular User: View Single Note
- **ID**: US-008
- **Description**: As a Regular User, I want to view the full content of a single note so that I can read it.
- **Acceptance criteria**:
  - User can select a note from their list to view its details.
  - The full title and content of the selected note are displayed.
  - User can only view their own notes. Attempting to access another user's note via URL manipulation should be denied.

### 10.9. Regular User: Update Note
- **ID**: US-009
- **Description**: As a Regular User, I want to update an existing note's title or content so that I can modify information.
- **Acceptance criteria**:
  - An option to edit a note is available when viewing or listing notes.
  - Selecting edit presents the note's current title and content in an editable form.
  - User can modify the title and/or content.
  - Upon saving, the changes are persisted and the `updated_at` timestamp is refreshed.
  - The user receives feedback that the note was updated successfully.
  - User can only update their own notes.

### 10.10. Regular User: Delete Note
- **ID**: US-010
- **Description**: As a Regular User, I want to delete one of my notes so that I can remove information I no longer need.
- **Acceptance criteria**:
  - An option to delete a note is available.
  - A confirmation prompt is displayed before permanent deletion.
  - Upon confirmation, the note is permanently removed from the system.
  - The user receives feedback that the note was deleted successfully.
  - The deleted note no longer appears in the user's list of notes.
  - User can only delete their own notes.

### 10.11. Regular User: Search Notes by Title
- **ID**: US-011
- **Description**: As a Regular User, I want to search my notes by title so that I can quickly find specific information.
- **Acceptance criteria**:
  - A search input field is available on the notes list page.
  - As the user types, the list of notes is filtered to show only notes where the title matches the search term (using a `LIKE` query, case-insensitive).
  - The search applies only to the logged-in user's notes.
  - If no notes match the search criteria, a clear message is displayed.

### 10.12. Admin: View All Users' Notes
- **ID**: US-012
- **Description**: As an Administrator, I want to view a list of all notes from all users so that I can oversee system content.
- **Acceptance criteria**:
  - A dedicated section in the admin dashboard lists all notes in the system.
  - Each note entry displays its title, content snippet, owner (user email or ID), and creation/update dates.
  - The list can be sorted and potentially filtered (e.g., by user).
  - Pagination is implemented for large numbers of notes.

### 10.13. Admin: Read Any User's Note
- **ID**: US-013
- **Description**: As an Administrator, I want to view the full content of any user's note so that I can perform administrative or support tasks.
- **Acceptance criteria**:
  - Admin can select any note from the "all notes" list or a user-specific list to view its full details.
  - The full title and content of the selected note are displayed.

### 10.14. Admin: Update Any User's Note
- **ID**: US-014
- **Description**: As an Administrator, I want to update any user's note so that I can correct information or perform administrative tasks.
- **Acceptance criteria**:
  - Admin has an option to edit any note.
  - Admin can modify the title and/or content.
  - Changes are saved, and the `updated_at` timestamp is refreshed.
  - An audit log (future consideration, not V1) might record that an admin made the change.

### 10.15. Admin: Delete Any User's Note
- **ID**: US-015
- **Description**: As an Administrator, I want to delete any user's note so that I can remove inappropriate or unnecessary content.
- **Acceptance criteria**:
  - Admin has an option to delete any note.
  - A confirmation prompt is displayed before deletion.
  - Upon confirmation, the note is permanently removed.
  - An audit log (future consideration, not V1) might record the deletion by an admin.

### 10.16. Admin: View User List
- **ID**: US-016
- **Description**: As an Administrator, I want to view a list of all user accounts so that I can manage them.
- **Acceptance criteria**:
  - Admin dashboard displays a list of all users.
  - Each user entry shows key information (e.g., email, role, status `is_active`, creation date).
  - The list is sortable and potentially searchable/filterable.

### 10.17. Admin: View User Details
- **ID**: US-017
- **Description**: As an Administrator, I want to view the detailed information of a specific user account.
- **Acceptance criteria**:
  - Admin can select a user from the list to view their full details.
  - Details include email, role, `is_active` status, `created_at`, `updated_at`, and potentially a count of their notes.

### 10.18. Admin: Manually Reset User Password
- **ID**: US-018
- **Description**: As an Administrator, I want to manually reset a user's password so that they can regain access if they've forgotten it.
- **Acceptance criteria**:
  - Admin can initiate a password reset for a selected user.
  - Admin can set a new temporary password for the user.
  - The system updates the user's `password_hash` with the new temporary password.
  - Admin is responsible for securely communicating this temporary password to the user out-of-band.
  - The user can log in with the temporary password.

### 10.19. Admin: Change User Role
- **ID**: US-019
- **Description**: As an Administrator, I want to change a user's role (e.g., from 'regular' to 'admin' or vice-versa) so that their permissions can be adjusted.
- **Acceptance criteria**:
  - Admin can select a user and change their role.
  - The system updates the user's `role` attribute.
  - The change in role immediately affects the user's permissions upon their next action or new session.
  - Care should be taken when promoting users to admin.

### 10.20. Admin: Disable/Enable User Account
- **ID**: US-020
- **Description**: As an Administrator, I want to disable or enable a user account so that I can control their access to the application.
- **Acceptance criteria**:
  - Admin can toggle an `is_active` status for a user account.
  - If an account is disabled (`is_active`=false), the user cannot log in. An appropriate message is shown on login attempt.
  - If an account is enabled (`is_active`=true), the user can log in as normal.
  - Disabling an account does not delete their data.

### 10.21. Admin: View System Statistics
- **ID**: US-021
- **Description**: As an Administrator, I want to view system statistics so that I can monitor application usage.
- **Acceptance criteria**:
  - Admin dashboard displays:
    - Total number of registered users.
    - Total number of notes in the system.
    - Average notes per user (total notes / total users).
    - Number of active users in the last 7 days (active = user has logged in).
  - Statistics are reasonably up-to-date.

### 10.22. Admin: View System Logs (User Logins)
- **ID**: US-022
- **Description**: As an Administrator, I want to view user login logs so that I can monitor access activity.
- **Acceptance criteria**:
  - Admin dashboard provides access to a log of user login events.
  - Each log entry includes at least: user identifier (email), timestamp of login, success/failure status.
  - Logs are presented in a readable format, possibly sortable by time.
  - (Consideration for Azure: these might be sourced from application logs integrated with Azure Monitor).

### 10.23. System: Responsive UI
- **ID**: US-023
- **Description**: As a User (Regular or Admin), I want the application to be responsive so that I can use it effectively on various devices (desktop, tablet, mobile).
- **Acceptance criteria**:
  - All UI elements and layouts adapt to different screen sizes.
  - Functionality is maintained across all supported device types.
  - Navigation is intuitive on smaller screens.
  - Tailwind CSS is correctly implemented to achieve responsiveness.

### 10.24. System: Error Handling and Feedback
- **ID**: US-024
- **Description**: As a User, I want to receive clear feedback and error messages so that I understand the application's state and can react to issues.
- **Acceptance criteria**:
  - Form submissions provide real-time validation feedback.
  - Successful operations are confirmed (e.g., via toast notifications).
  - Errors (e.g., API errors, validation failures) are displayed clearly as toast notifications or inline messages.
  - Loading states are shown during asynchronous operations.