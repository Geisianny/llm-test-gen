Feature: basket_management_story_processado

Scenario: Create a new basket asset
    Given there is a bank customer with an active account
    When the customer creates a new basket asset with a valid composition
    Then the system creates the basket asset
    And displays a confirmation message

Scenario: Add assets to an existing basket
    Given there is a bank customer with an existing basket asset
    And the basket asset has an initial composition
    When the customer adds new assets to the basket
    Then the system updates the basket composition
    And displays the updated basket details

Scenario: Decompose an existing basket asset
    Given there is a bank customer with an existing basket asset
    And the basket asset has a valid composition
    When the customer decomposes the basket asset
    Then the system removes the basket asset
    And distributes the underlying assets to the customer's account

Scenario: Rebalance an existing basket asset
    Given there is a bank customer with an existing basket asset
    And the basket asset has a valid composition
    When the customer requests rebalancing of the basket
    Then the system rebalances the basket asset according to the defined rules
    And displays the updated basket composition

Scenario: Attempt to create a basket asset with invalid composition
    Given there is a bank customer with an active account
    When the customer creates a new basket asset with an invalid composition
    Then the system denies the creation of the basket asset
    And displays an error message indicating the invalid composition
