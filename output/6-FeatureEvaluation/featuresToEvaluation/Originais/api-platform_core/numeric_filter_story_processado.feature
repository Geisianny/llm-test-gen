Feature: numeric_filter_story_processado

Scenario: Get collection by dummyPrice=9.99
    Tags: ['@createSchema']
    Given  there are 10 dummy objects with dummyPrice
    When  I send a "GET" request to "/dummies?dummyPrice=9.99"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the header "Content-Type" should be equal to "application/ld+json; charset=utf-8"
    And  the JSON should be valid according to this schema:



Scenario: Get collection by multiple dummyPrice
    Tags: ['@createSchema']
    Given  there are 10 dummy objects with dummyPrice
    When  I send a "GET" request to "/dummies?dummyPrice[]=9.99&dummyPrice[]=12.99"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the header "Content-Type" should be equal to "application/ld+json; charset=utf-8"
    And  the JSON should be valid according to this schema:



Scenario: Get collection by non-numeric dummyPrice=marty
    Given  there are 10 dummy objects with dummyPrice
    When  I send a "GET" request to "/dummies?dummyPrice=marty"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the header "Content-Type" should be equal to "application/ld+json; charset=utf-8"
    And  the JSON should be valid according to this schema:



Scenario: Get collection filtered using a name converter
    Tags: ['@createSchema']
    Given  there are 5 convertedInteger objects
    When  I send a "GET" request to "/converted_integers?name_converted[]=2&name_converted[]=3"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the header "Content-Type" should be equal to "application/ld+json; charset=utf-8"
    And  the JSON should be valid according to this schema:


