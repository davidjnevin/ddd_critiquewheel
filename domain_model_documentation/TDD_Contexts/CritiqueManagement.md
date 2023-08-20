## Critique Entity - Critique Management Bounded Context

### Attributes:

- **ID**: The UUID4 id of the critique.
- **Content_About**: What the work does or is, in one or two sentences.
- **Content_Successes**: The successes of the work. At least three.
- **Content_Weaknesses**: The weakest parts of the work. At least three.
- **Content_Ideas**: One or two ideas for the fastest and biggest improvements.
- **Status**: Current status of the critique (e.g., Active, Archived, Marked for Deletion, Pending Review, Rejected).
- **Submission Date**: Date when the critique was submitted.
- **last Updated Date**: Date when the critique was last updated.
- **Archive Date**: Date when the critique was archived (if applicable).
- **Member_id**: In this domain, member who wrote the critique.
- **Work_id**: The work this critique pertains to.

### Behaviors/Invariants:

1. **Creation**: A critique must have all four elements of content, about, successes, weaknesses and ideas.
1. **Submission Date**: Submission date should be set when the critique is submitted.
1. **Last Update Date**: Last updated date should be set when the critique is updated.
1. **Archiving**: A critique can be archived, which changes its status to "Archived" and sets the archive date.
1. **Mark for Deletion**: A critique can be marked for deletion, changing its status to "Marked for Deletion".
1. **Pending Review**: A critique can be marked pending review, changing its status to "Pending Review".
1. **Rejected**: A critique can be marked rejected, changing its status to "Rejected".
1. **Restoration**: An archived critique can be restored to active status, clearing the archive date.

### Unit Tests:

1. **Test Creation of Critique with All Required Content**:
   - **Description**: Ensure a critique can be created with all required content elements.
   - **Given**: All four elements of content (about, successes, weaknesses, and ideas) are provided.
   - **When**: A new critique is created.
   - **Then**: The critique is successfully created with the provided content.

1. **Test Creation of Critique with Missing Content**:
   - **Description**: Ensure a critique cannot be created if any of the required content elements are missing.
   - **Given**: One or more elements of content are missing.
   - **When**: An attempt is made to create a new critique.
   - **Then**: The creation fails with an appropriate error message.

1. **Test Setting Submission Date on Critique Creation**:
   - **Description**: Ensure the submission date is set when a critique is submitted.
   - **Given**: A new critique is being created.
   - **When**: The critique is submitted.
   - **Then**: The submission date is set to the current date.

1. **Test Updating Critique Content**:
   - **Description**: Ensure the last updated date is set when a critique's content is updated.
   - **Given**: An existing critique.
   - **When**: The content of the critique is updated.
   - **Then**: The last updated date is set to the current date.

1. **Test Archiving a Critique**:
   - **Description**: Ensure a critique can be archived and its status and archive date are updated.
   - **Given**: An active critique.
   - **When**: The critique is archived.
   - **Then**: The critique status is set to "Archived" and the archive date is set to the current date.

1. **Test Marking a Critique for Deletion**:
   - **Description**: Ensure a critique can be marked for deletion and its status is updated.
   - **Given**: An active critique.
   - **When**: The critique is marked for deletion.
   - **Then**: The critique status is set to "Marked for Deletion".

1. **Test Marking a Critique as Pending Review**:
   - **Description**: Ensure a critique can be marked as pending review and its status is updated.
   - **Given**: An active critique.
   - **When**: The critique is marked as pending review.
   - **Then**: The critique status is set to "Pending Review".

1. **Test Rejecting a Critique**:
   - **Description**: Ensure a critique can be rejected and its status is updated.
   - **Given**: A critique marked as "Pending Review".
   - **When**: The critique is rejected.
   - **Then**: The critique status is set to "Rejected".

1. **Test Restoring an Archived Critique**:
   - **Description**: Ensure an archived critique can be restored to active status and its archive date is cleared.
   - **Given**: An archived critique.
   - **When**: The critique is restored.
   - **Then**: The critique status is set to "Active" and the archive date is cleared.

