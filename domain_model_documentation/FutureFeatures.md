## Future Freatures

In particular order, just a doc to take ideas and notes.


1. **Account Lockout Mechanism**:
    This feature is designed to prevent brute-force attacks by temporarily locking out an account after a certain number of failed login attempts. Here's a breakdown:

    - **Threshold**: Define a threshold for the number of failed login attempts. For instance, after 5 failed attempts, the account gets locked.

    - **Lockout Duration**: Determine how long the account should be locked out. This could be a fixed duration (e.g., 30 minutes) or could increase with subsequent lockouts.

    - **Notification**: Notify the user when their account is locked, possibly through email. This serves as an alert in case someone else is trying to access their account.

    - **Manual Unlock**: Provide administrators with the ability to manually unlock accounts.

    - **Reset**: Optionally, after the lockout duration, you might want to offer users the option to unlock their account by verifying their identity (e.g., through email or SMS verification).

1. **Grouping of Permissions into Categories**:
    As your application grows, the number of permissions can become extensive. Grouping them into categories can make management more straightforward.

    - **Permission Categories**: Define broad categories for permissions. For instance, if you have a blogging platform, categories might include "Post Management", "Comment Management", "User Management", etc.

    - **Hierarchical Structure**: Within each category, you can have sub-categories. For example, under "Post Management", you might have "Create Post", "Edit Post", "Delete Post", etc.

    - **UI Implementation**: On the admin dashboard, when assigning permissions to roles or users, display permissions grouped by their categories. This makes the UI cleaner and more intuitive.

    - **Filtering & Searching**: Allow admins to filter or search permissions based on categories, making it easier to find and manage specific permissions.

**Next Steps**:
1. **Update the Data Model**: Modify your data models to accommodate these features. For the account lockout, you might need fields like `failed_login_attempts`, `last_failed_login`, and `account_locked_until`. For permission categories, you might introduce a new entity or table for "PermissionCategory" and associate permissions with them.

1. **Update Business Logic**: Implement the business logic for these features. For account lockout, after each failed login attempt, increment the `failed_login_attempts` and check if it exceeds the threshold. For permission categories, when creating or managing permissions, associate them with a category.

1. **Update the UI**: If you have a user interface for managing roles and permissions, update it to display permissions grouped by categories.

1. **Write Tests**: As with any new feature, write unit and integration tests to ensure everything works as expected and to catch any potential issues.

### Passwords in IAM

1. **Hashing**: Abstract out the hashing from the IAM model to allow for experimentation.

1. **Validation** Abstract out password validation.

1. **External IAM**: Explore possibility of using an external IAM/OAuth for better security and features.

### Loging

1. **External Solution**: Implment an external library to handle logging.

### Bio Photos

1. **Upload Bio Photos**: Allow users to upload bio photos.
