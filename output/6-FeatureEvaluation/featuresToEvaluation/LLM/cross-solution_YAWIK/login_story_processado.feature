Feature: login_story_processado

Scenario: Successful login with valid credentials
    Given there is a registered user with a valid email and password
    When the user logs in with the valid email
    And enters the correct password
    Then the system grants access to Yawik
    And displays the user's dashboard

Scenario: Login with incorrect password
    Given there is a registered user with a valid email and password
    When the user logs in with the valid email
    And enters an incorrect password
    Then the system denies access
    And displays a message indicating that the email or password is incorrect

Scenario: Login with unregistered email
    Given there is no registered user with the email "unregistered@example.com"
    When the user logs in with the email "unregistered@example.com"
    And enters a password
    Then the system denies access
    And displays a message indicating that the email or password is incorrect

Scenario: Login with invalid email format
    Given there is a registered user with a valid email and password
    When the user logs in with an invalid email format "invalidEmail"
    And enters the correct password
    Then the system denies access
    And displays a message indicating that the email format is invalid

Scenario: Login with empty credentials
    Given there is a registered user with a valid email and password
    When the user logs in with an empty email
    And enters an empty password
    Then the system denies access
    And displays a message indicating that email and password are required
