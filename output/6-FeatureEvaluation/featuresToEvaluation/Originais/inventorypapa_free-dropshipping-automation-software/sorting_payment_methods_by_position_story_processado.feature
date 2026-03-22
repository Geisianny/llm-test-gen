Feature: sorting_payment_methods_by_position_story_processado

Scenario: Payment methods are sorted by position in ascending order by default
    Tags: ['@ui']
    When  I browse payment methods
    Then  I should see 3 payment methods in the list
    And  the first payment method on the list should have name "Paypal Express Checkout"
    And  the last payment method on the list should have name "Cash on Delivery"



Scenario: Payment method added at no position is added as the last one
    Tags: ['@ui']
    Given  the store allows paying with "Credit Card"
    When  I browse payment methods
    Then  the last payment method on the list should have name "Credit Card"



Scenario: Payment method added at position 0 is added as the first one
    Tags: ['@ui']
    Given  the store also allows paying with "Credit Card" at position 0
    When  I browse payment methods
    Then  the first payment method on the list should have name "Credit Card"


