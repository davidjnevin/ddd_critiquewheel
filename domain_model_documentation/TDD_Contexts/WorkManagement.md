## Work Entity - Work Management Bounded Context

### Attributes:

- **ID**: The UUID4 id of the fictional work.
- **Title**: The title of the fictional work.
- **Content**: The actual content of the fictional work.
- **Age Restriction**: The age restriction applied to the fictional work. Options: None, Teen, Adult.
- **Genre**: The genre of the work. Selected from a predetermined list of 20 - 21 genres.
- **Status**: Current status of the work (e.g., Active, Archived, Marked for Deletion, Pending Review, Rejected).
- **Word Count**: Automatically calculated based on the content.
- **Submission Date**: Date when the work was submitted.
- **last Updated Date**: Date when the work was last updated.
- **Archive Date**: Date when the work was archived (if applicable).
- **Member_id**: In this domain, member who authored the work.

### Behaviors/Invariants:

1. **Creation**: A work must have a title, content, genre, age restriction and member_id to be created.
1. **Word Count Calculation**: Word count should be automatically calculated based on the content.
1. **Submission Date**: Submission date should be set when the work is submitted.
1. **Archiving**: A work can be archived, which changes its status to "Archived" and sets the archive date.
1. **Mark for Deletion**: A work can be marked for deletion, changing its status to "Marked for Deletion".
1. **Availability for Critique**: An archived work or a work marked for deletion should not be available for critique.
1. **Restoration**: An archived work can be restored to active status, clearing the archive date.

### Unit Tests:

1. **Test Work Creation with Valid Data**:
   - **Description**: Ensure that a work can be created with a valid title, content, age_restriction, genre and member_id.
   - **Given**: A title content, age_restricition, genre and member_id.
   - **When**: Creating a work.
   - **Then**: The work should be successfully created with the given data.

1. **Test Work Creation with Invalid Data**:
   - **Description**: Ensure that a work cannot be created without valid data.
   - **Given**: No title or no content or no genre, or no age_restriction, or no member_id.
   - **When**: Attempting to create a work.
   - **Then**: An error should be raised.

1. **Test Word Count Calculation**:
   - **Description**: Ensure that the word count is correctly calculated for a work.
   - **Given**: Content with X words.
   - **When**: Creating a work.
   - **Then**: The word count attribute should be X.

1. **Test Submission Date Setting**:
   - **Description**: Ensure that the submission date is set when a work is submitted.
   - **Given**: A new work.
   - **When**: It's submitted.
   - **Then**: The submission date should be the current date.

1. **Test Work Archiving**:
   - **Description**: Ensure that a work can be archived.
   - **Given**: An active work or a work marked for deletion.
   - **When**: Archiving the work.
   - **Then**: Its status should be "Archived" and the archive date should be set.

1. **Test Work Rejection**:
   - **Description**: Ensure that a work can be rejected.
   - **Given**: An active work or a work marked for deletion.
   - **When**: Rejecting the work.
   - **Then**: Its status should be "Rejected".

1. **Test Work Approved**:
   - **Description**: Ensure that a work can be approved.
   - **Given**: An pending work.
   - **When**: Approving the work.
   - **Then**: Its status should be "ACTIVE".

1. **Test Work Marked for Deletion**:
   - **Description**: Ensure that a work can be marked for deletion.
   - **Given**: An active work.
   - **When**: Marking it for deletion.
   - **Then**: Its status should be "Marked for Deletion".

1. **Test Archived Work Availability for Critique**:
   - **Description**: Ensure that an archived work is not available for critique.
   - **Given**: An archived work.
   - **When**: Checking availability for critique.
   - **Then**: False should be returned.

1. **Test Work Marked for Deletion Availability for Critique**:
   - **Description**: Ensure that a work marked for deletion is not available for critique.
   - **Given**: A work marked for deletion.
   - **When**: Checking availability for critique.
   - **Then**: False should be returned.

1. **Test Work Rejected Availability for Critique**:
   - **Description**: Ensure that a work rejectedt is not available for critique.
   - **Given**: A work marked rejected.
   - **When**: Attempting to critique it.
   - **Then**: An error should be raised.

1. **Test Archived Work Restoration**:
   - **Description**: Ensure that an archived work can be restored.
   - **Given**: An archived work.
   - **When**: Restoring it.
   - **Then**: Its status should be "Active" and the archive date should be cleared.


