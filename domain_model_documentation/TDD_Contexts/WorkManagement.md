## Work Entity - Work Management Bounded Context

### Attributes:

- **Title**: The title of the fictional work.
- **Content**: The actual content of the fictional work.
- **Word Count**: Automatically calculated based on the content.
- **Author**: Member who submitted the work.
- **Submission Date**: Date when the work was submitted.
- **Status**: Current status of the work (e.g., Active, Archived, Marked for Deletion).
- **Archive Date**: Date when the work was archived (if applicable).

### Behaviors/Invariants:

1. **Creation**: A work must have a title and content to be created.
2. **Word Count Calculation**: Word count should be automatically calculated based on the content.
3. **Submission Date**: Submission date should be set when the work is submitted.
4. **Archiving**: A work can be archived, which changes its status to "Archived" and sets the archive date.
5. **Mark for Deletion**: A work can be marked for deletion, changing its status to "Marked for Deletion".
6. **Availability for Critique**: An archived work or a work marked for deletion should not be available for critique.
7. **Restoration**: An archived work can be restored to active status, clearing the archive date.

### Unit Tests:

1. **Test Work Creation with Valid Data**:
   - **Description**: Ensure that a work can be created with a valid title and content.
   - **Given**: A title and content.
   - **When**: Creating a work.
   - **Then**: The work should be successfully created with the given title and content.

2. **Test Work Creation with Invalid Data**:
   - **Description**: Ensure that a work cannot be created without a title or content.
   - **Given**: No title or no content.
   - **When**: Attempting to create a work.
   - **Then**: An error should be raised.

3. **Test Word Count Calculation**:
   - **Description**: Ensure that the word count is correctly calculated for a work.
   - **Given**: Content with X words.
   - **When**: Creating a work.
   - **Then**: The word count attribute should be X.

4. **Test Submission Date Setting**:
   - **Description**: Ensure that the submission date is set when a work is submitted.
   - **Given**: A new work.
   - **When**: It's submitted.
   - **Then**: The submission date should be the current date.

5. **Test Work Archiving**:
   - **Description**: Ensure that a work can be archived.
   - **Given**: An active work or a work marked for deletion.
   - **When**: Archiving the work.
   - **Then**: Its status should be "Archived" and the archive date should be set.

6. **Test Work Marked for Deletion**:
   - **Description**: Ensure that a work can be marked for deletion.
   - **Given**: An active work.
   - **When**: Marking it for deletion.
   - **Then**: Its status should be "Marked for Deletion".

7. **Test Archived Work Availability for Critique**:
   - **Description**: Ensure that an archived work is not available for critique.
   - **Given**: An archived work.
   - **When**: Attempting to critique it.
   - **Then**: An error should be raised.

8. **Test Work Marked for Deletion Availability for Critique**:
   - **Description**: Ensure that a work marked for deletion is not available for critique.
   - **Given**: A work marked for deletion.
   - **When**: Attempting to critique it.
   - **Then**: An error should be raised.

9. **Test Archived Work Restoration**:
   - **Description**: Ensure that an archived work can be restored.
   - **Given**: An archived work.
   - **When**: Restoring it.
   - **Then**: Its status should be "Active" and the archive date should be cleared.


