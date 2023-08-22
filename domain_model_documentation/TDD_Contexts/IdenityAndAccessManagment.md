## Identity and Access Management (IAM) Bounded Context

### Overview:
The IAM context is responsible for managing member identity and controlling access within the system. It encompasses member registration, authentication, roles, permissions, and password management.

### Entities/Aggregates:

1. **Member**:
    - Represents a user in the system.
    - Attributes: ID (UUID), Email, Username, Password (hashed), Role, Status (Active, Inactive, Banned, Marked for Deletion), Last Login Date, Last Password Change Date.
    - Behaviors: Register, Login, Logout, Update Profile, Deactivate (self), Change Password.

1. **Role**:
    - Represents a role that a member can have.
    - Attributes: Role Name, Permissions.
    - Behaviors: Assign Permission, Remove Permission.

1. **Permission**:
    - Represents an action or access level that can be granted to a role.
    - Attributes: Permission Name, Description.

### Functionalities:

#### Member Registration:
- Members can register using their email, username, and password.
- A verification code is generated but the notification is managed by the Notification context.

#### Authentication:
- Members can log in using their email and password.
- Token-based authentication is used, with tokens expiring after 24 hours.

#### Roles and Permissions:
- Three static roles: Admin, Staff, and Member.
- Permissions are associated with roles, defining what actions a member can perform based on their role.

#### Password Management:
- Passwords must adhere to certain policies (e.g., minimum length, special characters).
- Members are prompted to change their password every 365 days.
- Password recovery is done via email reset only.

#### Member Management:
- Only Admins can activate, deactivate, or ban members.
- Members can deactivate their own accounts.
- When deactivated, a member's data is marked for deletion.

#### Audit and Logging:
- Member activities (e.g., login, logout, password change) are logged.
- Logs are retained for 90 days.

### Invariants:

1. A member's email and username must be unique.
1. Passwords must be stored securely (hashed).
1. A member can only have one active session at a time.
1. Permissions can only be assigned or removed by Admins.
1. Logs cannot be modified once created.

### Unit Tests:

1. **Title**: Member Registration
   - **Description**: Ensure a new member can successfully register.
   - **Given**: Registration details including email, password, and username.
   - **When**: The member attempts to register.
   - **Then**: A new member account should be created with the provided details.

1. **Title**: Member Login with Valid Credentials
   - **Description**: Ensure a member can log in with valid credentials.
   - **Given**: A registered member's email and password.
   - **When**: The member attempts to log in.
   - **Then**: The member should be successfully logged in.

1. **Title**: Member Login with Invalid Credentials
   - **Description**: Ensure a member cannot log in with invalid credentials.
   - **Given**: An email and incorrect password.
   - **When**: The member attempts to log in.
   - **Then**: The login should fail with an appropriate error message.

1. **Title**: Password Change with Correct Old Password
   - **Description**: Ensure a member can change their password by providing the correct old password.
   - **Given**: A member's old password and a new password.
   - **When**: The member attempts to change their password.
   - **Then**: The password should be successfully updated.

1. **Title**: Password Change with Incorrect Old Password
   - **Description**: Ensure a member cannot change their password without providing the correct old password.
   - **Given**: An incorrect old password and a new password.
   - **When**: The member attempts to change their password.
   - **Then**: The password change should fail with an appropriate error message.

1. **Title**: Assign Role to Member
   - **Description**: Ensure an admin can assign a role to a member.
   - **Given**: An admin user and a target member.
   - **When**: The admin assigns a role to the member.
   - **Then**: The member should have the assigned role.

1. **Title**: Member Self-Deactivation
   - **Description**: Ensure a member can deactivate their own account.
   - **Given**: A logged-in member.
   - **When**: The member chooses to deactivate their account.
   - **Then**: The member's status should be updated to "Inactive" or "Marked for Deletion".

1. **Title**: Admin Member Deactivation
   - **Description**: Ensure an admin can deactivate a member's account.
   - **Given**: An admin user and a target member.
   - **When**: The admin deactivates the member's account.
   - **Then**: The member's status should be updated to "Inactive" or "Marked for Deletion".

1. **Title**: Email Verification Code Generation
   - **Description**: Ensure a verification code is generated for email verification.
   - **Given**: A new member registration.
   - **When**: The member registers.
   - **Then**: A verification code should be generated (and ideally, sent via the Notification Context).

1. **Title**: Member Role Permission Check
   - **Description**: Ensure members can only perform actions they have permissions for.
   - **Given**: A member and an action that requires specific permissions.
   - **When**: The member attempts the action.
   - **Then**: The action should succeed or fail based on the member's permissions.

1. **Title**: Password Policy Enforcement
   - **Description**: Ensure that the password policy (e.g., minimum length, special characters) is enforced during registration and password change.
   - **Given**: A password that doesn't meet the policy requirements.
   - **When**: The member attempts to register or change their password.
   - **Then**: The operation should fail with an appropriate error message.

1. **Title**: Password Reset Request
   - **Description**: Ensure a member can request a password reset.
   - **Given**: A member's registered email address.
   - **When**: The member requests a password reset.
   - **Then**: A password reset token or link should be generated (and ideally, sent via the Notification Context).

1. **Title**: Password Reset with Valid Token
   - **Description**: Ensure a member can reset their password using a valid reset token.
   - **Given**: A valid password reset token and a new password.
   - **When**: The member attempts to reset their password.
   - **Then**: The password should be successfully updated.

1. **Title**: Password Reset with Invalid Token
   - **Description**: Ensure a member cannot reset their password using an invalid token.
   - **Given**: An invalid password reset token and a new password.
   - **When**: The member attempts to reset their password.
   - **Then**: The reset should fail with an appropriate error message.

1. **Title**: Member Activity Logging
   - **Description**: Ensure that member activities (e.g., login, logout, password change) are logged.
   - **Given**: A member performs an activity.
   - **When**: The activity is completed.
   - **Then**: The activity should be logged in the system.

1. **Title**: Role-Based Access Control
   - **Description**: Ensure that members can only access resources and perform actions based on their assigned roles.
   - **Given**: A member and a resource or action.
   - **When**: The member attempts to access the resource or perform the action.
   - **Then**: The access should be granted or denied based on the member's role and permissions.

1. **Title**: Email Update with Verification
   - **Description**: Ensure that when a member updates their email, it's verified before the change is finalized.
   - **Given**: A member's new email address.
   - **When**: The member updates their email.
   - **Then**: A verification code or link should be generated and sent to the new email address.

1. **Title**: Email Update with Existing Email
   - **Description**: Ensure a member cannot update their email to one that's already in use.
   - **Given**: An email address already associated with another member.
   - **When**: A different member attempts to update their email to the already-used address.
   - **Then**: The update should fail with an appropriate error message.

