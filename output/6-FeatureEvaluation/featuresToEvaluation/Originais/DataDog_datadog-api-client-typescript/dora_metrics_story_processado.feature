Feature: dora_metrics_story_processado

Scenario: Delete a deployment event returns "Accepted" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  new "DeleteDORADeployment" request
    And  a valid "appKeyAuth" key in the system
    And  request contains "deployment_id" parameter with value "NO_VALUE"
    When  the request is sent
    Then  the response status is 202 Accepted



Scenario: Delete a deployment event returns "Bad Request" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  new "DeleteDORADeployment" request
    And  request contains "deployment_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Delete a failure event returns "Accepted" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  new "DeleteDORAFailure" request
    And  a valid "appKeyAuth" key in the system
    And  request contains "failure_id" parameter with value "NO_VALUE"
    When  the request is sent
    Then  the response status is 202 Accepted



Scenario: Delete a failure event returns "Bad Request" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  new "DeleteDORAFailure" request
    And  a valid "appKeyAuth" key in the system
    And  request contains "failure_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get a deployment event returns "Bad Request" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "GetDORADeployment" request
    And  request contains "deployment_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get a deployment event returns "OK" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "GetDORADeployment" request
    And  request contains "deployment_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Get a failure event returns "Bad Request" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "GetDORAFailure" request
    And  request contains "failure_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get a failure event returns "OK" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "GetDORAFailure" request
    And  request contains "failure_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Get a list of deployment events returns "Bad Request" response
    Tags: ['@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "ListDORADeployments" request
    And  body with value {"data": {"attributes": {"limit": 10}}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get a list of deployment events returns "OK" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "ListDORADeployments" request
    And  body with value {"data": {"attributes": {"from": "2025-03-23T00:00:00Z", "limit": 1, "to": "2025-03-24T00:00:00Z"}, "type": "dora_deployments_list_request"}}
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Get a list of failure events returns "Bad Request" response
    Tags: ['@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "ListDORAFailures" request
    And  body with value {"data": {"attributes": {"limit": 10}}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get a list of failure events returns "OK" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  a valid "appKeyAuth" key in the system
    And  new "ListDORAFailures" request
    And  body with value {"data": {"attributes": {"from": "2025-03-23T00:00:00Z", "limit": 1, "to": "2025-03-24T00:00:00Z"}, "type": "dora_failures_list_request"}}
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Send a deployment event returns "Bad Request" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORADeployment" request
    And  body with value {"data": {"attributes": {}}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Send a deployment event returns "OK - but delayed due to incident" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORADeployment" request
    And  body with value {"data": {"attributes": {"custom_tags": ["language:java", "department:engineering"], "env": "staging", "finished_at": 1693491984000000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "service": "shopist", "started_at": 1693491974000000000, "team": "backend", "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 202 OK - but delayed due to incident



Scenario: Send a deployment event returns "OK" response
    Tags: ['@replay-only', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORADeployment" request
    And  body with value {"data": {"attributes": {"finished_at": 1693491984000000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "service": "shopist", "started_at": 1693491974000000000, "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Send a failure event returns "Bad Request" response
    Tags: ['@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORAIncident" request
    And  body with value {"data": {"attributes": {}}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Send a failure event returns "OK - but delayed due to incident" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORAFailure" request
    And  body with value {"data": {"attributes": {"custom_tags": ["language:java", "department:engineering"], "env": "staging", "finished_at": 1693491984000000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "name": "Webserver is down failing all requests.", "services": ["shopist"], "severity": "High", "started_at": 1693491974000000000, "team": "backend", "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 202 OK - but delayed due to incident



Scenario: Send a failure event returns "OK" response
    Tags: ['@replay-only', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORAIncident" request
    And  body with value {"data": {"attributes": {"finished_at": 1707842944600000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "name": "Webserver is down failing all requests", "services": ["shopist"], "severity": "High", "started_at": 1707842944500000000, "team": "backend", "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Send an incident event returns "Bad Request" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORAIncident" request
    And  body with value {"data": {"attributes": {"custom_tags": ["language:java", "department:engineering"], "env": "staging", "finished_at": 1693491984000000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "name": "Webserver is down failing all requests.", "services": ["shopist"], "severity": "High", "started_at": 1693491974000000000, "team": "backend", "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Send an incident event returns "OK - but delayed due to incident" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORAIncident" request
    And  body with value {"data": {"attributes": {"custom_tags": ["language:java", "department:engineering"], "env": "staging", "finished_at": 1693491984000000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "name": "Webserver is down failing all requests.", "services": ["shopist"], "severity": "High", "started_at": 1693491974000000000, "team": "backend", "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 202 OK - but delayed due to incident



Scenario: Send an incident event returns "OK" response
    Tags: ['@generated', '@skip', '@team:DataDog/ci-app-backend']
    Given  new "CreateDORAIncident" request
    And  body with value {"data": {"attributes": {"custom_tags": ["language:java", "department:engineering"], "env": "staging", "finished_at": 1693491984000000000, "git": {"commit_sha": "66adc9350f2cc9b250b69abddab733dd55e1a588", "repository_url": "https://github.com/organization/example-repository"}, "name": "Webserver is down failing all requests.", "services": ["shopist"], "severity": "High", "started_at": 1693491974000000000, "team": "backend", "version": "v1.12.07"}}}
    When  the request is sent
    Then  the response status is 200 OK


