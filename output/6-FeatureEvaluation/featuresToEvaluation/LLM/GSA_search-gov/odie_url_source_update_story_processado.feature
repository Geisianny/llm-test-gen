Feature: odie_url_source_update_story_processado

Scenario: Update document source for a valid affiliate
    Given there is an affiliate with the identifier "valid_affiliate"
    And the affiliate has indexed documents with source "rss"
    When the admin requests to update the document source to "manual" for the affiliate "valid_affiliate"
    And confirms the update operation
    Then the system queues a job to update the document source
    And displays a message confirming the update is in progress

Scenario: Update document source for an invalid affiliate
    Given there is no affiliate with the identifier "invalid_affiliate"
    When the admin requests to update the document source to "manual" for the affiliate "invalid_affiliate"
    And confirms the update operation
    Then the system displays an error message indicating the affiliate does not exist
    And does not queue a job to update the document source

Scenario: Cancel update document source operation
    Given there is an affiliate with the identifier "valid_affiliate"
    And the affiliate has indexed documents with source "rss"
    When the admin requests to update the document source to "manual" for the affiliate "valid_affiliate"
    And cancels the update operation
    Then the system does not queue a job to update the document source
    And displays a message confirming the update is cancelled

Scenario: Update document source job execution
    Given there is an affiliate with the identifier "valid_affiliate"
    And the affiliate has indexed documents with source "rss"
    And the admin has requested to update the document source to "manual" for the affiliate "valid_affiliate"
    And confirmed the update operation
    When the queued job to update the document source is executed
    Then the system updates the document source to "manual" for the affiliate "valid_affiliate"
    And displays a message confirming the update is successful

Scenario: Update document source with invalid new source
    Given there is an affiliate with the identifier "valid_affiliate"
    And the affiliate has indexed documents with source "rss"
    When the admin requests to update the document source to "invalid_source" for the affiliate "valid_affiliate"
    And confirms the update operation
    Then the system displays an error message indicating the new source is invalid
    And does not queue a job to update the document source
