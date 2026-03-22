Feature: trading_fees_spot_story_processado

Scenario: Order placement with sufficient balance
    Given there is a user with sufficient balance in their general account
    When the user places an order on a spot market
    Then the system reserves the required assets in the holding account
    And the order is accepted

Scenario: Order placement with insufficient balance
    Given there is a user with insufficient balance in their general account
    When the user places an order on a spot market
    Then the system rejects the order
    And displays a message indicating insufficient balance

Scenario: Trade occurrence with order fulfillment
    Given there is a user with an accepted order on a spot market
    And there is a matching trade for the order
    When the trade is executed
    Then the system releases the reserved assets
    And updates the user's general balance

Scenario: Trade occurrence with order cancellation
    Given there is a user with an accepted order on a spot market
    And there is no matching trade for the order
    When the order is cancelled
    Then the system releases the reserved assets
    And updates the user's general balance

Scenario: Order cancellation due to impossible fulfillment
    Given there is a user with an accepted order on a spot market
    And the order becomes impossible to fulfill
    When the system automatically cancels the order
    Then the system releases the reserved assets
    And updates the user's general balance
