Feature: logs_custom_destinations_story_processado

Scenario: Create a Basic HTTP custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"password": "datadog-custom-destination-password", "type": "basic", "username": "datadog-custom-destination-username"}, "endpoint": "https://example.com", "type": "http"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data" has field "id"
    And  the response "data.attributes.name" is equal to "Nginx logs"
    And  the response "data.attributes.query" is equal to "source:nginx"
    And  the response "data.attributes.forwarder_destination.type" is equal to "http"
    And  the response "data.attributes.forwarder_destination.endpoint" is equal to "https://example.com"
    And  the response "data.attributes.forwarder_destination.auth.type" is equal to "basic"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "username"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "password"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 2
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "datacenter"
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "ALLOW_LIST"



Scenario: Create a Custom Header HTTP custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"header_value": "my-secret", "type": "custom_header", "header_name": "MY-AUTHENTICATION-HEADER"}, "endpoint": "https://example.com", "type": "http"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data" has field "id"
    And  the response "data.attributes.name" is equal to "Nginx logs"
    And  the response "data.attributes.query" is equal to "source:nginx"
    And  the response "data.attributes.forwarder_destination.type" is equal to "http"
    And  the response "data.attributes.forwarder_destination.endpoint" is equal to "https://example.com"
    And  the response "data.attributes.forwarder_destination.auth.type" is equal to "custom_header"
    And  the response "data.attributes.forwarder_destination.auth.header_name" is equal to "MY-AUTHENTICATION-HEADER"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "header_value"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 2
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "datacenter"
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "ALLOW_LIST"



Scenario: Create a Microsoft Sentinel custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"type": "microsoft_sentinel", "tenant_id": "f3c9a8a1-4c2e-4d2e-b911-9f3c28c3c8b2", "client_id": "9a2f4d83-2b5e-429e-a35a-2b3c4182db71", "data_collection_endpoint": "https://my-dce-5kyl.eastus-1.ingest.monitor.azure.com", "data_collection_rule_id": "dcr-000a00a000a00000a000000aa000a0aa", "stream_name": "Custom-MyTable"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data" has field "id"
    And  the response "data.attributes.name" is equal to "Nginx logs"
    And  the response "data.attributes.query" is equal to "source:nginx"
    And  the response "data.attributes.forwarder_destination.type" is equal to "microsoft_sentinel"
    And  the response "data.attributes.forwarder_destination.tenant_id" is equal to "f3c9a8a1-4c2e-4d2e-b911-9f3c28c3c8b2"
    And  the response "data.attributes.forwarder_destination.client_id" is equal to "9a2f4d83-2b5e-429e-a35a-2b3c4182db71"
    And  the response "data.attributes.forwarder_destination.data_collection_endpoint" is equal to "https://my-dce-5kyl.eastus-1.ingest.monitor.azure.com"
    And  the response "data.attributes.forwarder_destination.data_collection_rule_id" is equal to "dcr-000a00a000a00000a000000aa000a0aa"
    And  the response "data.attributes.forwarder_destination.stream_name" is equal to "Custom-MyTable"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 2
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "datacenter"
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "ALLOW_LIST"



Scenario: Create a Splunk custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"access_token": "my-access-token", "endpoint": "https://example.com", "type": "splunk_hec"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data" has field "id"
    And  the response "data.attributes.name" is equal to "Nginx logs"
    And  the response "data.attributes.query" is equal to "source:nginx"
    And  the response "data.attributes.forwarder_destination.type" is equal to "splunk_hec"
    And  the response "data.attributes.forwarder_destination.endpoint" is equal to "https://example.com"
    And  the response "data.attributes.forwarder_destination" does not have field "access_token"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 2
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "datacenter"
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "ALLOW_LIST"



Scenario: Create a custom destination returns "Bad Request" response
    Tags: ['@skip-java', '@skip-python', '@skip-rust', '@skip-typescript', '@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"name": "Nginx logs"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Create a custom destination returns "Conflict" response
    Tags: ['@generated', '@skip', '@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": true, "forward_tags": true, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"password": "datadog-custom-destination-password", "type": "basic", "username": "datadog-custom-destination-username"}, "endpoint": "https://example.com", "type": "http"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 409 Conflict



Scenario: Create a custom destination returns "OK" response
    Tags: ['@generated', '@skip', '@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": true, "forward_tags": true, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"password": "datadog-custom-destination-password", "type": "basic", "username": "datadog-custom-destination-username"}, "endpoint": "https://example.com", "type": "http"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 200 OK



Scenario: Create an Elasticsearch custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "CreateLogsCustomDestination" request
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"username": "my-username", "password": "my-password"}, "index_name": "nginx-logs", "index_rotation": "yyyy-MM-dd", "endpoint": "https://example.com", "type": "elasticsearch"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data" has field "id"
    And  the response "data.attributes.name" is equal to "Nginx logs"
    And  the response "data.attributes.query" is equal to "source:nginx"
    And  the response "data.attributes.forwarder_destination.type" is equal to "elasticsearch"
    And  the response "data.attributes.forwarder_destination.endpoint" is equal to "https://example.com"
    And  the response "data.attributes.forwarder_destination.index_name" is equal to "nginx-logs"
    And  the response "data.attributes.forwarder_destination.index_rotation" is equal to "yyyy-MM-dd"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "username"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "password"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 2
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "datacenter"
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "ALLOW_LIST"



Scenario: Delete a custom destination returns "Bad Request" response
    Tags: ['@generated', '@skip', '@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "DeleteLogsCustomDestination" request
    And  request contains "custom_destination_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Delete a custom destination returns "Not Found" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "DeleteLogsCustomDestination" request
    And  request contains "custom_destination_id" parameter with value "does-not-exist"
    When  the request is sent
    Then  the response status is 404 Not found



Scenario: Delete a custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "DeleteLogsCustomDestination" request
    And  there is a valid "custom_destination" in the system
    And  request contains "custom_destination_id" parameter from "custom_destination.data.id"
    When  the request is sent
    Then  the response status is 204 OK



Scenario: Get a custom destination returns "Bad Request" response
    Tags: ['@generated', '@skip', '@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "GetLogsCustomDestination" request
    And  request contains "custom_destination_id" parameter from "REPLACE.ME"
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Get a custom destination returns "Not Found" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "GetLogsCustomDestination" request
    And  request contains "custom_destination_id" parameter with value "does-not-exist"
    When  the request is sent
    Then  the response status is 404 Not found



Scenario: Get a custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "GetLogsCustomDestination" request
    And  there is a valid "custom_destination" in the system
    And  request contains "custom_destination_id" parameter from "custom_destination.data.id"
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data.id" is equal to "{{ custom_destination.data.id }}"
    And  the response "data.attributes.name" is equal to "{{ custom_destination.data.attributes.name }}"
    And  the response "data.attributes.query" is equal to "{{ custom_destination.data.attributes.query }}"
    And  the response "data.attributes.forwarder_destination.type" is equal to "{{ custom_destination.data.attributes.forwarder_destination.type }}"
    And  the response "data.attributes.forwarder_destination.endpoint" is equal to "{{ custom_destination.data.attributes.forwarder_destination.endpoint }}"
    And  the response "data.attributes.forwarder_destination.auth.type" is equal to "{{ custom_destination.data.attributes.forwarder_destination.auth.type }}"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "username"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "password"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 1
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "{{ custom_destination.data.attributes.forward_tags_restriction_list_type }}"



Scenario: Get all custom destinations returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "ListLogsCustomDestinations" request
    And  there is a valid "custom_destination" in the system
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data" has item with field "type" with value "custom_destination"
    And  the response "data" has item with field "id" with value "{{ custom_destination.data.id }}"
    And  the response "data" has item with field "attributes.name" with value "{{ custom_destination.data.attributes.name }}"
    And  the response "data" has item with field "attributes.query" with value "{{ custom_destination.data.attributes.query }}"
    And  the response "data" has item with field "attributes.forwarder_destination.type" with value "{{ custom_destination.data.attributes.forwarder_destination.type }}"
    And  the response "data" has item with field "attributes.forwarder_destination.endpoint" with value "{{ custom_destination.data.attributes.forwarder_destination.endpoint }}"
    And  the response "data" has item with field "attributes.forwarder_destination.auth.type" with value "{{ custom_destination.data.attributes.forwarder_destination.auth.type }}"
    And  the response "data" has item with field "attributes.enabled" with value false
    And  the response "data" has item with field "attributes.forward_tags" with value false
    And  the response "data" has item with field "attributes.forward_tags_restriction_list_type" with value "{{ custom_destination.data.attributes.forward_tags_restriction_list_type }}"



Scenario: Update a custom destination returns "Bad Request" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "UpdateLogsCustomDestination" request
    And  there is a valid "custom_destination" in the system
    And  request contains "custom_destination_id" parameter from "custom_destination.data.id"
    And  body with value {"data": {"attributes": {"forward_tags_restriction_list_type": "this_list_type_does_not_exist"}, "type": "custom_destination", "id": "{{ custom_destination.data.id }}" }}
    When  the request is sent
    Then  the response status is 400 Bad Request



Scenario: Update a custom destination returns "Conflict" response
    Tags: ['@skip', '@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "UpdateLogsCustomDestination" request
    And  request contains "custom_destination_id" parameter from "REPLACE.ME"
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"password": "datadog-custom-destination-password", "type": "basic", "username": "datadog-custom-destination-username"}, "endpoint": "https://example.com", "type": "http"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination"}}
    When  the request is sent
    Then  the response status is 409 Conflict



Scenario: Update a custom destination returns "Not Found" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "UpdateLogsCustomDestination" request
    And  request contains "custom_destination_id" parameter with value "id-from-non-existing-custom-destination"
    And  body with value {"data": {"attributes": {"enabled": false, "forward_tags": false, "forward_tags_restriction_list": ["datacenter", "host"], "forward_tags_restriction_list_type": "ALLOW_LIST", "forwarder_destination": {"auth": {"type": "basic", "username": "datadog-custom-destination-username", "password": "datadog-custom-destination-password"}, "endpoint": "https://example.com", "type": "http"}, "name": "Nginx logs", "query": "source:nginx"}, "type": "custom_destination", "id": "id-from-non-existing-custom-destination" }}
    When  the request is sent
    Then  the response status is 404 Not Found



Scenario: Update a custom destination returns "OK" response
    Tags: ['@team:DataDog/logs-backend', '@team:DataDog/logs-forwarding']
    Given  new "UpdateLogsCustomDestination" request
    And  there is a valid "custom_destination" in the system
    And  request contains "custom_destination_id" parameter from "custom_destination.data.id"
    And  body with value {"data": {"attributes": {"name": "Nginx logs (Updated)", "query": "source:nginx", "enabled":false, "forward_tags":false, "forward_tags_restriction_list_type":"BLOCK_LIST"}, "type": "custom_destination", "id": "{{ custom_destination.data.id }}"}}
    When  the request is sent
    Then  the response status is 200 OK
    And  the response "data.type" is equal to "custom_destination"
    And  the response "data.id" is equal to "{{ custom_destination.data.id }}"
    And  the response "data.attributes.name" is equal to "Nginx logs (Updated)"
    And  the response "data.attributes.query" is equal to "{{ custom_destination.data.attributes.query }}"
    And  the response "data.attributes.forwarder_destination.type" is equal to "{{ custom_destination.data.attributes.forwarder_destination.type }}"
    And  the response "data.attributes.forwarder_destination.endpoint" is equal to "{{ custom_destination.data.attributes.forwarder_destination.endpoint }}"
    And  the response "data.attributes.forwarder_destination.auth.type" is equal to "{{ custom_destination.data.attributes.forwarder_destination.auth.type }}"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "username"
    And  the response "data.attributes.forwarder_destination.auth" does not have field "password"
    And  the response "data.attributes.enabled" is false
    And  the response "data.attributes.forward_tags" is false
    And  the response "data.attributes.forward_tags_restriction_list" has length 1
    And  the response "data.attributes.forward_tags_restriction_list" array contains value "host"
    And  the response "data.attributes.forward_tags_restriction_list_type" is equal to "{{ custom_destination.data.attributes.forward_tags_restriction_list_type }}"


