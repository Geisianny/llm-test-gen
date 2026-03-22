Feature: pay_invoice_story_processado

Scenario: Full payment of an invoice in the same currency
    Given there is an invoice with a total amount of $100 in USD
    And the invoice status is "open"
    When the user makes a payment of $100 in USD
    Then the invoice status is updated to "paid"
    And the residual amount is $0

Scenario: Partial payment of an invoice in the same currency
    Given there is an invoice with a total amount of $100 in USD
    And the invoice status is "open"
    When the user makes a payment of $50 in USD
    Then the residual amount is $50
    And the invoice status remains "open"

Scenario: Full payment of an invoice in a different currency
    Given there is an invoice with a total amount of €100 in EUR
    And the invoice status is "open"
    When the user makes a payment of $110 in USD, equivalent to €100
    Then the invoice status is updated to "paid"
    And the residual amount is €0

Scenario: Multiple partial payments of an invoice
    Given there is an invoice with a total amount of $100 in USD
    And the invoice status is "open"
    When the user makes a payment of $30 in USD
    And makes another payment of $40 in USD
    Then the residual amount is $30
    And the invoice status remains "open"

Scenario: Overpayment of an invoice
    Given there is an invoice with a total amount of $100 in USD
    And the invoice status is "open"
    When the user makes a payment of $120 in USD
    Then the residual amount is -$20
    And the invoice status is updated to "paid" with a credit note of $20
