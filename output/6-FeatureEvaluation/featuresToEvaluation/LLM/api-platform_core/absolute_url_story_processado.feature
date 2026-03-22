Feature: absolute_url_story_processado

Scenario: Published resource with absolute URL
    Given there is a published resource with the identifier "123"
    When the client requests the resource "123"
    Then the system returns the resource with an absolute URL
    And the URL is in the format "https://example.com/resources/123"

Scenario: Collection of resources with absolute URLs
    Given there is a collection of published resources
    When the client requests the collection
    Then the system returns a list of resources with absolute URLs
    And each URL is in the format "https://example.com/resources/{id}"

Scenario: Relation with absolute URL
    Given there is a published resource with a related resource
    When the client requests the resource
    Then the system returns the related resource with an absolute URL
    And the URL is in the format "https://example.com/related-resources/{id}"

Scenario: Client navigates through absolute URLs
    Given there is a published resource with an absolute URL "https://example.com/resources/123"
    When the client navigates to the URL "https://example.com/resources/123"
    Then the system returns the resource with the identifier "123"
    And the response contains the expected data

Scenario: Client submits information using absolute URL
    Given there is a published resource with an absolute URL "https://example.com/resources/123"
    When the client submits information to the URL "https://example.com/resources/123"
    Then the system processes the submitted information
    And the resource with the identifier "123" is updated accordingly
