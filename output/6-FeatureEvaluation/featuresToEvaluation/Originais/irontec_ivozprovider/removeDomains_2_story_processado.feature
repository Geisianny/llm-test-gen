Feature: removeDomains_2_story_processado

Scenario: Delete a domain
    Tags: ['@createSchema']
    Given  I add Authorization header
    When  I add "Content-Type" header equal to "application/json"
    And  I add "Accept" header equal to "application/json"
    And  I send a "DELETE" request to "/domains/1"
    Then  the response status code should be 405


