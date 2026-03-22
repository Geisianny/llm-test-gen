Feature: samples_story_processado

Scenario: Create a new partner
    Given there is no existing partner with the name "Test Partner"
    When the user creates a new partner with the name "Test Partner"
    Then the system creates the partner successfully
    And the partner is visible in the partner list

Scenario: Update an existing partner
    Given there is an existing partner with the name "Test Partner"
    When the user updates the partner with the new name "Updated Test Partner"
    Then the system updates the partner successfully
    And the partner is visible with the new name "Updated Test Partner"

Scenario: Validate an invoice
    Given there is an existing invoice with the status "draft"
    When the user validates the invoice
    Then the system updates the invoice status to "open"
    And the invoice is marked as validated

Scenario: Use stored variables across scenarios
    Given there is an existing partner with the name "Test Partner"
    And the partner's ID is stored as a variable "partner_id"
    When the user creates a new invoice for the partner with ID "partner_id"
    Then the system creates the invoice successfully
    And the invoice is associated with the partner "Test Partner"

Scenario: Locate a record using helpers
    Given there is an existing partner with the name "Test Partner"
    When the user searches for the partner using the helper "partner_name"
    Then the system locates the partner successfully
    And the partner's details are displayed correctly
