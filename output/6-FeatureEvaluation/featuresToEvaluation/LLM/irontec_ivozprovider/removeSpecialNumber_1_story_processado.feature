Feature: removeSpecialNumber_1_story_processado

Scenario: Delete a special number successfully
    Given there is a super admin with valid credentials
    And there is a special number with ID "123"
    When the super admin sends a DELETE request to the special number API with ID "123"
    Then the system returns an HTTP 204 status code
    And the special number with ID "123" is deleted

Scenario: Attempt to delete a non-existent special number
    Given there is a super admin with valid credentials
    And there is no special number with ID "123"
    When the super admin sends a DELETE request to the special number API with ID "123"
    Then the system returns an HTTP 404 status code
    And displays a message indicating that the special number was not found

Scenario: Delete a special number without authentication
    Given there is no authenticated user
    And there is a special number with ID "123"
    When an unauthenticated user sends a DELETE request to the special number API with ID "123"
    Then the system returns an HTTP 401 status code
    And displays a message indicating that authentication is required

Scenario: Delete a special number with insufficient permissions
    Given there is a user with insufficient permissions
    And there is a special number with ID "123"
    When the user sends a DELETE request to the special number API with ID "123"
    Then the system returns an HTTP 403 status code
    And displays a message indicating that the user lacks the necessary permissions

Scenario: Delete a special number with invalid ID
    Given there is a super admin with valid credentials
    When the super admin sends a DELETE request to the special number API with an invalid ID "abc"
    Then the system returns an HTTP 400 status code
    And displays a message indicating that the ID is invalid
