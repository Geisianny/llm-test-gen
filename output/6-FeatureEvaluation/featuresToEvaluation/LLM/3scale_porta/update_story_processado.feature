Feature: update_story_processado

Scenario: Update notification preferences with valid selections
    Given the provider user is on the notification preferences page
    And there are notification types available for selection
    When the provider user selects some notification types
    And submits the updated preferences
    Then the system updates the notification preferences
    And displays a success confirmation message

Scenario: Update notification preferences with no selections
    Given the provider user is on the notification preferences page
    And there are notification types available for selection
    When the provider user deselects all notification types
    And submits the updated preferences
    Then the system updates the notification preferences
    And displays a success confirmation message

Scenario: Cancel update notification preferences
    Given the provider user is on the notification preferences page
    And there are notification types available for selection
    When the provider user makes changes to the notification preferences
    And cancels the update
    Then the system does not update the notification preferences
    And redirects the provider user to the previous page

Scenario: Update notification preferences with invalid input
    Given the provider user is on the notification preferences page
    And there are notification types available for selection
    When the provider user makes invalid changes to the notification preferences
    And submits the updated preferences
    Then the system displays an error message
    And does not update the notification preferences

Scenario: Initial notification preferences display
    Given the provider user is on the notification preferences page
    And there are notification types available for selection
    Then the system displays the current notification preferences
    And the notification types are correctly checked or unchecked according to the user's current preferences
