## Rating Entity - Rating Management Bounded Context

### Attributes:

- **ID**: The UUID4 id of the rating.
- **Score**: Numeric value representing the rating (e.g., 1 to 5).
- **Comment**: Optional textual feedback about the critique.
- **Date**: Date when the rating was given.
- **Critique_id**: The critique this rating pertains to.
- **Member_id**: In this domain, member who gave the rating.

### Behaviors/Invariants:

1. **Creation**: A rating must have a score and be associated with a critique.
2. **Score Range**: The score must be within a predefined range (e.g., 1 to 5).
3. **Update**: A rating can be updated, but the associated critique cannot be changed.
4. **Deletion**: A rating can be deleted if necessary.

### Unit Tests:

1. **Test Creation of Rating with Valid Score**:
   - **Description**: Ensure a rating can be created with a valid score.
   - **Given**: A valid score and associated critique.
   - **When**: A new rating is created.
   - **Then**: The rating is successfully created with the provided score.

2. **Test Creation of Rating with Invalid Score**:
   - **Description**: Ensure a rating cannot be created with an invalid score.
   - **Given**: An invalid score (outside the predefined range).
   - **When**: An attempt is made to create a new rating.
   - **Then**: The creation fails with an appropriate error message.

3. **Test Updating Rating Score**:
   - **Description**: Ensure a rating's score can be updated.
   - **Given**: An existing rating.
   - **When**: The score of the rating is updated.
   - **Then**: The updated score is reflected in the rating.

4. **Test Preventing Update of Associated Critique**:
   - **Description**: Ensure the associated critique of a rating cannot be changed.
   - **Given**: An existing rating.
   - **When**: An attempt is made to change the associated critique.
   - **Then**: The update fails with an appropriate error message.

5. **Test Deletion of Rating**:
   - **Description**: Ensure a rating can be deleted.
   - **Given**: An existing rating.
   - **When**: The rating is deleted.
   - **Then**: The rating is removed from the system.

6. **Test Optional Comment on Rating**:
   - **Description**: Ensure a comment can be added to a rating.
   - **Given**: An existing rating without a comment.
   - **When**: A comment is added to the rating.
   - **Then**: The comment is reflected in the rating.
