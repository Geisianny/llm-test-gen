Feature: discount_percent_gross_action_story_processado

Scenario: Apply 10 percent discount on a single item cart
    Given there is an active voucher-type rule with a 10 percent discount
    And the cart contains one item priced at 100.00
    When the user applies the voucher code
    Then the cart total is recalculated to 90.00
    And the item price is adjusted to 90.00

Scenario: Apply 10 percent discount on a multiple item cart
    Given there is an active voucher-type rule with a 10 percent discount
    And the cart contains two items priced at 100.00 and 200.00
    When the user applies the voucher code
    Then the cart total is recalculated to 270.00
    And the item prices are adjusted to 90.00 and 180.00

Scenario: Apply voucher code with invalid code
    Given there is an active voucher-type rule with a 10 percent discount
    And the cart contains one item priced at 100.00
    When the user applies an invalid voucher code
    Then the cart total remains 100.00
    And the system displays a message indicating that the voucher code is invalid

Scenario: Apply voucher code on an empty cart
    Given there is an active voucher-type rule with a 10 percent discount
    And the cart is empty
    When the user applies the voucher code
    Then the system displays a message indicating that the cart is empty
    And the cart total remains 0.00

Scenario: Remove voucher code from cart
    Given there is an active voucher-type rule with a 10 percent discount
    And the cart contains one item priced at 100.00
    And the voucher code is applied
    When the user removes the voucher code
    Then the cart total is recalculated to 100.00
    And the item price is adjusted to 100.00
