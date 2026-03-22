Feature: cli_story_processado

Scenario: Display help message for init command
    Given the user is using the Karma CLI
    When the user executes the command "karma init --help"
    Then the system displays a detailed help message for the init command
    And includes information on available options and usage

Scenario: Execute init command successfully
    Given the user is using the Karma CLI
    When the user executes the command "karma init"
    Then the system initializes a new Karma configuration
    And displays a confirmation message indicating successful initialization

Scenario: Display error message for unknown command
    Given the user is using the Karma CLI
    When the user executes the command "karma unknown"
    Then the system displays an error message indicating that the command is unknown
    And suggests using the "--help" option for available commands

Scenario: Start Karma server successfully
    Given the user has a valid Karma configuration
    When the user executes the command "karma start"
    Then the system starts the Karma server
    And displays a message confirming the server is running

Scenario: Display error message for missing configuration
    Given the user is using the Karma CLI without a configuration file
    When the user executes the command "karma start"
    Then the system displays an error message indicating that the configuration file is missing
    And suggests creating a configuration file or using the "init" command to initialize one
