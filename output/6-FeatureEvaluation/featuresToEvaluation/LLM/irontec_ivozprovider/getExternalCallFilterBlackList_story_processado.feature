Feature: getExternalCallFilterBlackList_story_processado

Scenario: Retrieve external call filter blacklists with valid authentication
    Given there is a client admin with a valid authentication token
    When the client admin sends a GET request to retrieve external call filter blacklists
    Then the system returns a JSON response with the list of blacklists
    And the response status code is 200

Scenario: Retrieve external call filter blacklists with invalid authentication
    Given there is a client admin with an invalid authentication token
    When the client admin sends a GET request to retrieve external call filter blacklists
    Then the system returns an error response
    And the response status code is 401

Scenario: Retrieve a specific external call filter blacklist by ID
    Given there is a client admin with a valid authentication token
    And there is an existing external call filter blacklist with ID "123"
    When the client admin sends a GET request to retrieve the blacklist with ID "123"
    Then the system returns a JSON response with the blacklist details
    And the response status code is 200

Scenario: Retrieve a non-existent external call filter blacklist by ID
    Given there is a client admin with a valid authentication token
    And there is no existing external call filter blacklist with ID "456"
    When the client admin sends a GET request to retrieve the blacklist with ID "456"
    Then the system returns an error response
    And the response status code is 404

Scenario: Retrieve external call filter blacklists with missing authentication token
    Given there is a client admin without an authentication token
    When the client admin sends a GET request to retrieve external call filter blacklists
    Then the system returns an error response
    And the response status code is 401
