Feature: cli_story_processado

Scenario: Top-level CLI help
    When  I execute Karma with arguments: "--help"
    Then  the stdout is exactly:



Scenario: Current version
    When  I execute Karma with arguments: "--version"
    Then  the stdout matches RegExp:



Scenario: Error when command is unknown
    When  I execute Karma with arguments: "strat"
    Then  the stderr is exactly:



Scenario: No error when unknown option and argument are passed in
    Given  a configuration with:
    When  I execute Karma with arguments: "start sandbox/karma.conf.js unknown-argument --unknown-option"
    Then  it passes with:



Scenario: Init command help
    When  I execute Karma with arguments: "init --help"
    Then  the stdout is exactly:



Scenario: Start command help
    When  I execute Karma with arguments: "start --help"
    Then  the stdout is exactly:



Scenario: Run command help
    When  I execute Karma with arguments: "run --help"
    Then  the stdout is exactly:



Scenario: Stop command help
    When  I execute Karma with arguments: "stop --help"
    Then  the stdout is exactly:



Scenario: Completion command help
    When  I execute Karma with arguments: "completion --help"
    Then  the stdout is exactly:


