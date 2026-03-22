Feature: status_story_processado

Scenario: Add status to comment in community context
    Given the user is an administrator of a community
    And the community has a comment section
    When the user adds a status to a comment
    Then the comment is updated with the selected status
    And the status is visible to other community members

Scenario: Attempt to add status to comment in personal profile context
    Given the user is on their personal profile
    And the personal profile has a comment section
    When the user attempts to add a status to a comment
    Then the system denies the action
    And displays a message indicating that status addition is not allowed on personal profiles

Scenario: Configure new status in community settings
    Given the user is an administrator of a community
    And the community has a status configuration section
    When the user configures a new status
    Then the new status is available for use in the community's comment section
    And the status is listed in the community's status configuration

Scenario: Add status to comment without permission
    Given the user is a member of a community but not an administrator
    And the community has a comment section
    When the user attempts to add a status to a comment
    Then the system denies the action
    And displays a message indicating that the user lacks permission to add status

Scenario: Successfully configure multiple statuses in community settings
    Given the user is an administrator of a community
    And the community has a status configuration section
    When the user configures multiple new statuses
    Then all new statuses are available for use in the community's comment section
    And all statuses are listed in the community's status configuration
