# Writing Club Software Documentation

## Introduction

This document provides a comprehensive overview of the Writing Club software, detailing its domain model, user stories, use cases, and other relevant information to guide the development process.

## Domain Model

### Bounded Contexts:

- **Work Management**: Deals with the submission, storage, and retrieval of fictional works.

- **Critique Management**: Handles the submission, storage, and assignment of critiques.

- **Rating Management**: Manages the submission, storage, and retrieval of ratings for critiques. Calculates and updates the reputation of members.

- **Monetization**: Handles aspects related to paid critiques, including setting prices, managing transactions, and tracking paid critique requests.

- **Member Management**: Responsible for all member-related operations and data, including registration, authentication, profile management, tracking submission eligibility, and managing member preferences or settings.

### Credit System:

Members earn and spend credits based on the word length of works they critique and submit, respectively. The system ensures fairness and encourages members to critique longer works.

## User Stories:

### Submission & Critique:

- As a member, I want to submit my fictional work so that it can be critiqued by others.
- As a member, I want to critique other members' works to earn credits and help them improve.

### Credit System:

- As a member, I want to earn credits based on the word length of the works I critique.
- As a member, I want to spend credits to submit my works for critique, with the cost based on my work's word length.
- As a member, I want to view my current credit balance to understand my contribution and submission capabilities.

### Reputation & Monetization:

- As a member with a high reputation, I want to offer paid critique services to earn money for my expertise.
- As a member, I want to purchase critiques from high-reputation members using real money.

### Member Management:

- As a new user, I want to register as a member to participate in the writing club.
- As a member, I want to log in to access my works, critiques, and credit balance.
- As a member, I want to update my profile to reflect my writing preferences and expertise.

### Critique Rating:

- As a member, after receiving a critique, I want to rate the quality of the critique to provide feedback and influence the reputation of the reviewer.

## Use Cases:

### Submitting a Work:

- **Actor**: Member
- **Scenario**:
  1. Member logs in.
  2. Member navigates to submission page.
  3. Member uploads work.
  4. System calculates required credits.
  5. System checks credit balance.
  6. System confirms or denies submission based on credits.
- **Preconditions**: Member is logged in.
- **Postconditions**: Work is submitted and available for critique; credits are deducted.

### Critiquing a Work:

- **Actor**: Member
- **Scenario**:
  1. Member logs in.
  2. Member selects a work to critique.
  3. Member submits critique.
  4. System calculates earned credits.
  5. System updates member's credit balance.
- **Preconditions**: Member is logged in.
- **Postconditions**: Critique is submitted; credits are added to member's balance.

### Viewing Credit Balance:

- **Actor**: Member
- **Scenario**:
  1. Member logs in.
  2. Member navigates to profile page.
  3. System displays current credit balance.
- **Preconditions**: Member is logged in.
- **Postconditions**: Member views current credit balance.

### Rating a Critique:

- **Actor**: Member (who received the critique)
- **Scenario**:
  1. Member logs in.
  2. Member navigates to their submitted works.
  3. Member selects a work that has been critiqued.
  4. Member views the critique.
  5. Member rates the critique on a predefined scale (e.g., 1 to 5 stars).
  6. System updates the reviewer's reputation based on the rating.
- **Preconditions**: Member has received a critique on one of their works.
- **Postconditions**: Critique is rated, and reviewer's reputation is updated.

(Additional use cases can be added for other functionalities.)
