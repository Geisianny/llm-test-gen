Feature: 0068-MATC-073_story_processado

Scenario: Post-only limit order does not cross existing orders
    Given there are existing orders on the book that do not cross
    When a user places a LIMIT order with post-only flag set to TRUE
    Then the order is placed fully on the book
    And the order status is "Active"

Scenario: Post-only limit order crosses existing orders
    Given there are existing orders on the book that cross
    When a user places a LIMIT order with post-only flag set to TRUE
    Then the order is rejected
    And the system displays a message indicating that the order crosses existing orders

Scenario: Post-only limit GTT order is placed on the book
    Given there are no existing orders on the book that cross
    When a user places a LIMIT GTT order with post-only flag set to TRUE
    Then the order is placed fully on the book
    And the order status is "Active"

Scenario: Post-only limit GTC order is placed on the book
    Given there are no existing orders on the book that cross
    When a user places a LIMIT GTC order with post-only flag set to TRUE
    Then the order is placed fully on the book
    And the order status is "Active"

Scenario: Post-only limit GFN order is placed on the book
    Given there are no existing orders on the book that cross
    When a user places a LIMIT GFN order with post-only flag set to TRUE
    Then the order is placed fully on the book
    And the order status is "Active"
