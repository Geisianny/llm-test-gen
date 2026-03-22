Feature: sale_story_processado

Scenario: Create a new sales order
    Given there is a valid customer
    When the administrator creates a new sales order for the customer
    And adds a product to the order with a valid quantity
    Then the system creates a sales order with the correct total amount
    And the sales order is in the "draft" state

Scenario: Confirm a sales order
    Given there is a sales order in the "draft" state
    When the administrator confirms the sales order
    Then the system updates the sales order state to "confirmed"
    And generates a corresponding document for the sales order

Scenario: Generate invoice from a confirmed sales order
    Given there is a confirmed sales order
    When the administrator generates an invoice from the sales order
    Then the system creates an invoice with the correct amount
    And the invoice is in the "open" state

Scenario: Cancel an invoice generated from a sales order
    Given there is an invoice generated from a sales order
    And the invoice is in the "open" state
    When the administrator cancels the invoice
    Then the system updates the invoice state to "cancelled"
    And the corresponding sales order remains in the "confirmed" or "done" state depending on the configuration

Scenario: Validate accounting entries for a sales order
    Given there is a sales order that has been confirmed and invoiced
    And the invoice has been paid
    When the administrator checks the accounting entries for the sales order
    Then the system displays the correct accounting entries for the transaction
    And the accounting entries are properly balanced and recorded
