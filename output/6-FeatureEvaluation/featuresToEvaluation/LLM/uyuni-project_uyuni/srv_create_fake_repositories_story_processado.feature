Feature: srv_create_fake_repositories_story_processado

Scenario: Create a fake repository for RPM format
    Given there is an authorized user
    And the system has a child channel for RPM format
    When the user creates a fake repository for the RPM child channel
    Then the system creates the fake repository
    And associates it with the RPM child channel

Scenario: Create a fake repository for AppStream format
    Given there is an authorized user
    And the system has a child channel for AppStream format
    When the user creates a fake repository for the AppStream child channel
    Then the system creates the fake repository
    And associates it with the AppStream child channel

Scenario: Create a fake repository with metadata verification disabled
    Given there is an authorized user
    And the system has a child channel
    When the user creates a fake repository for the child channel with metadata verification disabled
    Then the system creates the fake repository
    And the repository has metadata verification disabled

Scenario: Create a fake repository for multiple child channels
    Given there is an authorized user
    And the system has multiple child channels
    When the user creates a fake repository for each child channel
    Then the system creates a fake repository for each child channel
    And associates each repository with its respective child channel

Scenario: Attempt to create a fake repository without authorization
    Given there is an unauthorized user
    And the system has a child channel
    When the user attempts to create a fake repository for the child channel
    Then the system denies the request
    And displays a message indicating that the user is not authorized
