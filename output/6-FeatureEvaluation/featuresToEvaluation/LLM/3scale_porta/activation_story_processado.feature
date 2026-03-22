Feature: activation_story_processado

Scenario: Successful account activation
    Given there is a registered user with an unactivated account
    And the user has received an activation token via email
    When the user activates their account using the received token
    Then the system marks the user's account as activated
    And the user can log in to their account

Scenario: Login before account activation
    Given there is a registered user with an unactivated account
    When the user attempts to log in to their account
    Then the system denies access
    And displays a message indicating that the account is not activated

Scenario: Account activation with invalid token
    Given there is a registered user with an unactivated account
    When the user attempts to activate their account using an invalid token
    Then the system denies activation
    And displays a message indicating that the activation token is invalid

Scenario: Login after successful account activation
    Given there is a registered user with an activated account
    When the user logs in to their account with valid credentials
    Then the system grants access
    And displays a message confirming successful login

Scenario: Multiple activation attempts with same token
    Given there is a registered user with an unactivated account
    And the user has received an activation token via email
    When the user activates their account using the received token
    And attempts to activate their account again using the same token
    Then the system denies the second activation attempt
    And displays a message indicating that the account is already activated
