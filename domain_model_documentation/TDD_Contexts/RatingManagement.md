## Rating Entity - Rating Management Bounded Context

### Attributes:

- **ID**: The UUID4 id of the rating.
- **Score**: Numeric value representing the rating (e.g., 1 to 5).
- **Comment**: Optional textual feedback about the critique.
- **Submission_date**: Date when the rating was given.
- **Last Updated Date**: Date when the rating was last updated.
- **Critique_id**: The critique this rating pertains to.
- **Member_id**: In this domain, member who gave the rating.
- **Status**: The rating status can be ACTIVE, PENDING_REVIEW or MARKED_FOR_DELETION.

### Behaviors/Invariants:

1. **Creation**: A rating must have a score and be associated with a critique.
1. **Score Range**: The score must be within a predefined range (e.g., 1 to 5).
1. **Update**: A rating can be updated, but the associated critique cannot be changed.
1. **Deletion**: A rating can be marked for deletion if necessary.

### Unit Tests:

1. **Test Creation of Rating with Valid Score**:
   - **Description**: Ensure a rating can be created with a valid score.
   - **Given**: A valid score and associated critique.
   - **When**: A new rating is created.
   - **Then**: The rating is successfully created with the provided score.

1. **Test Creation of Rating with Invalid Score**:
   - **Description**: Ensure a rating cannot be created with an invalid score.
   - **Given**: An invalid score (outside the predefined range).
   - **When**: An attempt is made to create a new rating.
   - **Then**: The creation fails with an appropriate error message.

1. **Test Updating Rating Score**:
   - **Description**: Ensure a rating's score can be updated.
   - **Given**: An existing rating.
   - **When**: The score of the rating is updated.
   - **Then**: The updated score is reflected in the rating.

1. **Test Preventing Update of Associated Critique**:
   - **Description**: Ensure the associated critique of a rating cannot be changed.
   - **Given**: An existing rating.
   - **When**: An attempt is made to change the associated critique.
   - **Then**: The update fails with an appropriate error message.

1. **Test Optional Comment on Rating**:
   - **Description**: Ensure a comment can be added to a rating.
   - **Given**: An existing rating without a comment.
   - **When**: A comment is added to the rating.
   - **Then**: The comment is reflected in the rating.

1. **Test Mark Critique as Pending Review**:
   - **Description**: Ensure a critique status can be marked as pending review.
   - **Given**: An existing critique.
   - **When**: A critique is marked pending review.
   - **Then**: The status is PENDING_REVIEW.

1. **Test Restore Critique**:
   - **Description**: Ensure a critique status can be restored to ACTIVE.
   - **Given**: An existing critique with status MARKED_FOR_DELETION, or PENDING_REVIEW, or REJECTED.
   - **When**: A critique is restored.
   - **Then**: The status is ACTIVE.

1. **Test Mark Critique as Marked for Deletion**:
   - **Description**: Ensure a critique status can be marked for deletion.
   - **Given**: An existing critique.
   - **When**: A critique is marked for deletion.
   - **Then**: The status is MARKED_FOR_DELETION

1. **Test Rejection of Rating**:
   - **Description**: Ensure a rating can be rejected.
   - **Given**: An existing rating.
   - **When**: The rating is rejected.
   - **Then**: The rating is marked REJECTED.
