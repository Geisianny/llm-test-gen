Feature: not_discountable_discount_amount_action_story_processado

Scenario: Apply non-discountable rule to cart
    Given there is a product with a price of $100
    And a non-discountable price rule is applied to the product
    When the customer adds the product to the cart
    Then the cart total remains $100

Scenario: Non-discountable rule overrides voucher discount
    Given there is a product with a price of $100
    And a non-discountable price rule is applied to the product
    And there is an active voucher offering a $20 discount
    When the customer adds the product to the cart
    And applies the voucher to the cart
    Then the cart total remains $100

Scenario: Non-discountable rule does not affect other products
    Given there are two products, product A with a price of $100 and product B with a price of $50
    And a non-discountable price rule is applied to product A
    And there is an active voucher offering a $10 discount on product B
    When the customer adds both products to the cart
    And applies the voucher to the cart
    Then the cart total is $140

Scenario: Multiple non-discountable rules on the same product
    Given there is a product with a price of $100
    And multiple non-discountable price rules are applied to the product
    When the customer adds the product to the cart
    Then the cart total remains $100

Scenario: Non-discountable rule and percentage discount voucher
    Given there is a product with a price of $100
    And a non-discountable price rule is applied to the product
    And there is an active voucher offering a 20% discount
    When the customer adds the product to the cart
    And applies the voucher to the cart
    Then the cart total remains $100
