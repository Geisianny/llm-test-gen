Feature: user_controller_donation_story_processado

Scenario: View donation details in account profile
    Given there is a logged-in adherent with an active donation
    When the adherent views their account profile
    Then the system displays the donation details
    And shows the upcoming due date

Scenario: Display multiple active donations
    Given there is a logged-in adherent with multiple active donations
    When the adherent views their account profile
    Then the system displays all active donations
    And shows the respective upcoming due dates

Scenario: No donations to display
    Given there is a logged-in adherent with no active donations
    When the adherent views their account profile
    Then the system displays a message indicating no donations

Scenario: Cancel an active donation
    Given there is a logged-in adherent with an active donation
    When the adherent requests to cancel the donation
    Then the system displays a confirmation message
    And the donation is marked as cancelled

Scenario: Successful cancellation confirmation
    Given there is a logged-in adherent with an active donation that is being cancelled
    When the adherent confirms the cancellation
    Then the system displays a message confirming successful cancellation
    And the donation is no longer active
