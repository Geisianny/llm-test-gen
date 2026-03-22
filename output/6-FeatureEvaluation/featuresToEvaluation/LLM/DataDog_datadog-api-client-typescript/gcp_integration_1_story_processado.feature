Feature: gcp_integration_1_story_processado

Scenario: Create a new STS service account
    Given the Datadog API is available
    And there are no existing STS service accounts with the name "new-sts-account"
    When the user creates a new STS service account with the name "new-sts-account"
    And configures the filters "filter1, filter2"
    And enables CSPM and Security Command Center
    Then the system creates the STS service account successfully
    And returns the details of the newly created STS service account

Scenario: List existing STS service accounts
    Given the Datadog API is available
    And there are existing STS service accounts with names "sts-account-1, sts-account-2"
    When the user requests to list all STS service accounts
    Then the system returns a list of existing STS service accounts
    And includes "sts-account-1" and "sts-account-2" in the list

Scenario: Update an existing STS service account
    Given the Datadog API is available
    And there is an existing STS service account with the name "existing-sts-account"
    When the user updates the STS service account "existing-sts-account"
    And changes the filters to "new-filter1, new-filter2"
    And disables CSPM
    Then the system updates the STS service account successfully
    And returns the updated details of the STS service account

Scenario: Delete an existing STS service account
    Given the Datadog API is available
    And there is an existing STS service account with the name "sts-account-to-delete"
    When the user deletes the STS service account "sts-account-to-delete"
    Then the system deletes the STS service account successfully
    And returns a confirmation of the deletion

Scenario: Attempt to create a duplicate STS service account
    Given the Datadog API is available
    And there is an existing STS service account with the name "duplicate-sts-account"
    When the user creates a new STS service account with the name "duplicate-sts-account"
    Then the system denies the creation
    And returns an error message indicating that an STS service account with the same name already exists
