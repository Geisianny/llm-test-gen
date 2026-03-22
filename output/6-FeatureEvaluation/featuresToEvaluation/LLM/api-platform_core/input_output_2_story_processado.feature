Feature: input_output_2_story_processado

Scenario: Successful password reset using DTO
    Given there is a registered user with the email "user@example.com"
    When the client sends a password reset request with the email "user@example.com"
    And includes a valid JSON payload
    Then the system returns a 201 status code
    And includes the dispatch timestamp in the response

Scenario: Password reset with non-existent user
    Given there is no registered user with the email "nonexistent@example.com"
    When the client sends a password reset request with the email "nonexistent@example.com"
    And includes a valid JSON payload
    Then the system returns a 404 status code
    And includes a problem+json formatted response

Scenario: Invalid JSON payload for password reset
    Given there is a registered user with the email "user@example.com"
    When the client sends a password reset request with the email "user@example.com"
    And includes an invalid JSON payload
    Then the system returns a 400 status code
    And includes an error message indicating invalid JSON

Scenario: Missing content header for DTO
    Given there is a registered user with the email "user@example.com"
    When the client sends a password reset request with the email "user@example.com"
    And omits the content header
    Then the system returns a 415 status code
    And includes an error message indicating unsupported media type

Scenario: Successful DTO processing with application/json
    Given there is a registered user with the email "user@example.com"
    When the client sends a request with a valid DTO in application/json format
    Then the system processes the DTO successfully
    And returns a response indicating successful processing
