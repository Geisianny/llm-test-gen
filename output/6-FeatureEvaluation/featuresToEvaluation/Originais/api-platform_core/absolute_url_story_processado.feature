Feature: absolute_url_story_processado

Scenario: I should be able to GET a collection of Objects with Absolute Urls
    Tags: ['@createSchema']
    Given  there are 1 absoluteUrlDummy objects with a related absoluteUrlRelationDummy
    And  I add "Accept" header equal to "application/hal+json"
    And  I send a "GET" request to "/absolute_url_dummies"
    And  the JSON should be equal to:



Scenario: I should be able to POST an object using an Absolute Url
    Given  I add "Accept" header equal to "application/hal+json"
    And  I add "Content-Type" header equal to "application/json"
    And  I send a "POST" request to "/absolute_url_relation_dummies" with body:
    Then  the response status code should be 201
    And  the JSON should be equal to:



Scenario: I should be able to GET an Item with Absolute Urls
    Given  I add "Accept" header equal to "application/hal+json"
    And  I add "Content-Type" header equal to "application/json"
    And  I send a "GET" request to "/absolute_url_dummies/1"
    And  the JSON should be equal to:



Scenario: I should be able to GET resources with Absolute Urls
    Given  I add "Accept" header equal to "application/hal+json"
    And  I add "Content-Type" header equal to "application/json"
    And  I send a "GET" request to "/absolute_url_relation_dummies/1/absolute_url_dummies"
    And  the JSON should be equal to:


