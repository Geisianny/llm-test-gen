Feature: service_level_objectives_1_story_processado

Scenario: Create a new SLO report returns "Bad Request" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "CreateSLOReportJob" enabled
    And  new "CreateSLOReportJob" request
    And  body with value {"data": {"attributes": {"from_ts": {{ timestamp('now - 40d') }},  "to_ts": {{ timestamp('now') }}, "query": "slo_type:metric \"SLO Reporting Test\"", "interval": "bad-interval"}}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Create a new SLO report returns "OK" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "CreateSLOReportJob" enabled
    And  new "CreateSLOReportJob" request
    And  body with value {"data": {"attributes": {"from_ts": {{ timestamp('now - 40d') }},  "to_ts": {{ timestamp('now') }}, "query": "slo_type:metric \"SLO Reporting Test\"", "interval": "monthly", "timezone": "America/New_York"}}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "report_id"



Scenario: Get SLO report returns "Bad Request" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "GetSLOReport" enabled
    And  new "GetSLOReport" request
    And  request contains "report_id" parameter with value "invalid-report-id"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get SLO report returns "Not Found" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "GetSLOReport" enabled
    And  new "GetSLOReport" request
    And  request contains "report_id" parameter with value "2b468c54-f2a7-11ee-b0b4-ffe56bb6ad43"
    When  the request is sent
    Then  the response status is 404 Not Found



Scenario: Get SLO report returns "OK" response
    Tags: ['@skip', '@team:DataDog/slo-app']
    Given  operation "GetSLOReport" enabled
    And  new "GetSLOReport" request
    And  request contains "report_id" parameter with value "9fb2dc2a-ead0-11ee-a174-9fe3a9d7627f"
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Get SLO report status returns "Bad Request" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "GetSLOReportJobStatus" enabled
    And  new "GetSLOReportJobStatus" request
    And  request contains "report_id" parameter with value "invalid-report-id"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get SLO report status returns "Not Found" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "GetSLOReportJobStatus" enabled
    And  new "GetSLOReportJobStatus" request
    And  request contains "report_id" parameter with value "2b468c54-f2a7-11ee-b0b4-ffe56bb6ad43"
    When  the request is sent
    Then  the response status is 404 Not Found



Scenario: Get SLO report status returns "OK" response
    Tags: ['@team:DataDog/slo-app']
    Given  operation "GetSLOReportJobStatus" enabled
    And  new "GetSLOReportJobStatus" request
    And  there is a valid "report" in the system
    And  request contains "report_id" parameter from "report.data.id"
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "report_id"


