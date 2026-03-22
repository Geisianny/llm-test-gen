Feature: _0296Unbundling_story_processado

Scenario: Create unbundling document for a bundle with multiple components
    Given there is a bundle product with multiple component items
    And the sales manager has the necessary permissions
    When the sales manager creates an unbundling document for the bundle product
    Then the system generates the unbundling document with the component items
    And the document status is set to "Draft"

Scenario: Unbundling document creation fails due to missing bundle product
    Given there is no bundle product with the specified ID
    And the sales manager has the necessary permissions
    When the sales manager attempts to create an unbundling document for the non-existent bundle product
    Then the system displays an error message indicating that the bundle product does not exist

Scenario: Successful unbundling document generation with automatic item key creation
    Given there is a bundle product with component items that require automatic item key generation
    And the sales manager has the necessary permissions
    When the sales manager creates an unbundling document for the bundle product
    Then the system generates the unbundling document with the component items and automatically creates item keys
    And the document status is set to "Draft"

Scenario: Unbundling document creation with pre-defined specifications
    Given there is a bundle product with pre-defined specifications for unbundling
    And the sales manager has the necessary permissions
    When the sales manager creates an unbundling document for the bundle product using the pre-defined specifications
    Then the system generates the unbundling document with the component items and applies the pre-defined specifications
    And the document status is set to "Draft"

Scenario: Unbundling document approval and inventory update
    Given there is an unbundling document in "Draft" status
    And the sales manager has the necessary permissions
    When the sales manager approves the unbundling document
    Then the system updates the inventory levels for the component items across different warehouse profiles
    And the document status is set to "Approved"
