Feature: launcher-error_story_processado

Scenario: Broken Browser
    Given  a configuration with:
    When  I start Karma
    Then  it fails with like:


