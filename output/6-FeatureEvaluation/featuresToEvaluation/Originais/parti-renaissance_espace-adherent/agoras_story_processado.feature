Feature: agoras_story_processado

Scenario: As a non logged-in user I can not see Agoras
    When  I send a "GET" request to "/api/v3/agoras"
    Then  the response status code should be 401



Scenario: As a logged-in user I can retrieve active Agoras
    Given  I am logged with "michelle.dufour@example.ch" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "GET" request to "/api/v3/agoras"
    Then  the response status code should be 200
    And  the JSON should be equal to:



Scenario: As a logged-in user I can filter Agoras by name
    Given  I am logged with "michelle.dufour@example.ch" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "GET" request to "/api/v3/agoras?name=Première"
    Then  the response status code should be 200
    And  the JSON should be equal to:



Scenario: As a logged-in user (not adherent) I can not join an Agora
    Given  I am logged with "carl999@example.fr" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "POST" request to "/api/v3/agoras/82ad6422-cb82-4c04-b478-bfb421c740e0/join"
    Then  the response status code should be 403



Scenario: As a logged-in adherent I can not join an Agora I am already member of
    Given  I am logged with "luciole1989@spambox.fr" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "POST" request to "/api/v3/agoras/82ad6422-cb82-4c04-b478-bfb421c740e0/join"
    Then  the response status code should be 400
    And  the JSON should be equal to:



Scenario: As a logged-in adherent I can not join an unpublished Agora
    Given  I am logged with "luciole1989@spambox.fr" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "POST" request to "/api/v3/agoras/c3d0fb57-1ce9-441a-9978-8445fc01fa5c/join"
    Then  the response status code should be 404



Scenario: As a logged-in adherent I can not join an Agora that is already full of members
    Given  I am logged with "adherent-male-51@en-marche-dev.fr" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "POST" request to "/api/v3/agoras/75d47004-db80-4586-8fc5-e97cec58e5b4/join"
    Then  the response status code should be 400
    And  the JSON should be equal to:



Scenario: As a logged-in adherent I can join an Agora
    Given  I am logged with "adherent-male-51@en-marche-dev.fr" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "POST" request to "/api/v3/agoras/82ad6422-cb82-4c04-b478-bfb421c740e0/join"
    Then  the response status code should be 201
    And  the JSON should be equal to:



Scenario: As a logged-in adherent I can not leave an Agora I am not member of
    Given  I am logged with "gisele-berthoux@caramail.com" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "DELETE" request to "/api/v3/agoras/82ad6422-cb82-4c04-b478-bfb421c740e0/leave"
    Then  the response status code should be 400
    And  the JSON should be equal to:



Scenario: As a logged-in user I can leave an Agora
    Given  I am logged with "luciole1989@spambox.fr" via OAuth client "JeMengage Mobile" with scope "jemarche_app"
    When  I send a "DELETE" request to "/api/v3/agoras/82ad6422-cb82-4c04-b478-bfb421c740e0/leave"
    Then  the response status code should be 200
    And  the JSON should be equal to:



Scenario: As a logged-in Agora Manager I can see the Agoras I am manager of
    Given  I am logged with "luciole1989@spambox.fr" via OAuth client "JeMengage Web" with scope "jemengage_admin"
    When  I send a "GET" request to "/api/v3/agoras?scope=agora_general_secretary"
    Then  the response status code should be 200
    And  the JSON should be equal to:



Scenario: As a logged-in Agora Manager I can see the members of an Agora
    Given  I am logged with "michelle.dufour@example.ch" via OAuth client "JeMengage Web" with scope "jemengage_admin"
    When  I send a "GET" request to "/api/v3/adherents?scope=agora_president&agora_uuids[]=82ad6422-cb82-4c04-b478-bfb421c740e0"
    Then  the response status code should be 200
    And  the JSON should be a superset of:


