Feature: tag_story_processado

Scenario: Execute a test in Firefox with version, with JavaScript tag
    Given  a configuration with:
    When  I start Karma
    Then  it passes with like:



Scenario: Execute a test in ChromeHeadless with version, without JavaScript tag
    Given  a configuration with:
    When  I start Karma
    Then  it passes with:



Scenario: Execute a test in Firefox without version, without JavaScript tag
    Given  a configuration with:
    When  I start Karma
    Then  it passes with:



Scenario: Execute a test in ChromeHeadless without version, without JavaScript tag
    Given  a configuration with:
    When  I start Karma
    Then  it passes with:


