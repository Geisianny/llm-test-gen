Feature: scopes_story_processado

Scenario: 
    When  I am logged with "deputy@en-marche-dev.fr" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scopes"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the JSON should be equal to:



Scenario: 
    When  I am logged with "deputy@en-marche-dev.fr" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scope/deputy"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the JSON should be equal to:



Scenario: 
    When  I am logged with "deputy@en-marche-dev.fr" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scope/national"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the JSON should be equal to:



Scenario: 
    When  I am logged with "gisele-berthoux@caramail.com" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scopes"
    Then  the response status code should be 200
    And  the JSON should be equal to:



Scenario: 
    When  I am logged with "gisele-berthoux@caramail.com" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scope/delegated_d2315289-a3fd-419c-a3dd-3e1ff71b754d"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the JSON should be equal to:



Scenario: 
    When  I am logged with "senateur@en-marche-dev.fr" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scope/delegated_08f40730-d807-4975-8773-69d8fae1da74"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the JSON should be equal to:



Scenario: 
    Given  I am logged with "adherent-male-55@en-marche-dev.fr" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scope/animator"
    Then  the response status code should be 200
    And  the response should be in JSON
    And  the JSON should be equal to:



Scenario: 
    When  I am logged with "gisele-berthoux@caramail.com" via OAuth client "JeMengage Web"
    When  I send a "GET" request to "/api/v3/profile/me/scope/test"
    Then  the response status code should be 403


