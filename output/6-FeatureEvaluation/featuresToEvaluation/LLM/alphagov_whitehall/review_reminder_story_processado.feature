Feature: review_reminder_story_processado

Scenario: Set a review date for a new document
    Given there is a document without a review date
    When the editor sets a review date for the document
    And the review date is "2024-03-15"
    Then the system displays the review date "2024-03-15" on the edition summary page
    And the document has a configured reminder for "2024-03-15"

Scenario: Edit the review date for an existing document
    Given there is a document with a review date "2024-03-15"
    When the editor updates the review date to "2024-06-15"
    Then the system displays the review date "2024-06-15" on the edition summary page
    And the document has a configured reminder for "2024-06-15"

Scenario: Remove the review date for a document
    Given there is a document with a review date "2024-03-15"
    When the editor removes the review date
    Then the system does not display a review date on the edition summary page
    And the document does not have a configured reminder

Scenario: Attempt to set an invalid review date
    Given there is a document without a review date
    When the editor sets a review date for the document
    And the review date is "invalid-date"
    Then the system displays an error message indicating that the review date is invalid

Scenario: Set a review date in the past
    Given there is a document without a review date
    When the editor sets a review date for the document
    And the review date is "2022-01-01"
    Then the system displays a warning message indicating that the review date is in the past
    And the review date "2022-01-01" is still saved for the document
