Feature: in-arrears-purchase_story_processado

Scenario: COGS posting with existing inventory sold short
    Given there are sales recorded without associated costs
    And a purchase invoice is available with the cost of goods
    When the purchase invoice is posted
    Then the system automatically posts the COGS
    And updates the accounting records accordingly

Scenario: No COGS posting without inventory sold short
    Given there are no sales recorded without associated costs
    And a purchase invoice is available with the cost of goods
    When the purchase invoice is posted
    Then the system does not post COGS
    And the accounting records remain unchanged regarding COGS

Scenario: COGS posting with multiple sales without costs
    Given there are multiple sales recorded without associated costs
    And a purchase invoice is available with the cost of goods
    When the purchase invoice is posted
    Then the system automatically posts the COGS for all applicable sales
    And updates the accounting records accordingly

Scenario: COGS posting with sales entered before purchase
    Given sales are recorded before the corresponding purchase invoice
    When the purchase invoice is posted
    Then the system automatically posts the COGS
    And the accounting records reflect the correct COGS

Scenario: COGS posting when transactions are out-of-order
    Given transactions are entered out-of-order during periodic bookkeeping
    And there are sales recorded without associated costs
    When the purchase invoice is posted
    Then the system automatically posts the COGS
    And the accounting records are updated to reflect the correct COGS
