Feature: min_bootstrap_negative_story_processado

Scenario: Register a machine with valid parameters
    Given there is an authorized user
    And there is no registered machine with the name "minion1"
    When the user registers a new machine with the name "minion1" and valid credentials
    Then the system registers the machine successfully
    And displays a message confirming successful registration

Scenario: Register a machine that is already registered
    Given there is an authorized user
    And there is a registered machine with the name "minion1"
    When the user registers a new machine with the name "minion1" and valid credentials
    Then the system denies registration
    And displays a message indicating that the machine is already registered

Scenario: Register a machine with non-existent name
    Given there is an authorized user
    When the user registers a new machine with a non-existent name "nonexistentminion"
    And valid credentials
    Then the system denies registration
    And displays a message indicating that the machine name does not exist

Scenario: Register a machine with incorrect access credentials
    Given there is an authorized user
    And there is a machine with the name "minion1"
    When the user registers a new machine with the name "minion1"
    And incorrect credentials
    Then the system denies registration
    And displays a message indicating that the access credentials are incorrect

Scenario: Register a machine with an invalid port
    Given there is an authorized user
    And there is a machine with the name "minion1" on an invalid port
    When the user registers a new machine with the name "minion1" and valid credentials on the invalid port
    Then the system denies registration
    And displays a message indicating that the connection cannot be established on the specified port
