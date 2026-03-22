Feature: removeSpecialNumber_1_story_processado

Scenario: Remove a special numbers
    Tags: ['@createSchema']
    Given  I add Authorization header
    When  I add "Content-Type" header equal to "application/json"
    And  I add "Accept" header equal to "application/json"
    And  I send a "DELETE" request to "/special_numbers/1"
    Then  the response status code should be 204


