Feature: sorting_payment_methods_by_position_story_processado

Scenario: Sort payment methods in ascending order by default
    Given there are multiple payment methods with different positions
    When the administrator views the payment methods
    Then the system displays the payment methods in ascending order by position

Scenario: Sort payment methods in ascending order manually
    Given there are multiple payment methods with different positions
    When the administrator chooses to sort payment methods by position
    Then the system displays the payment methods in ascending order by position

Scenario: Add new payment method to the end of the list
    Given there are multiple payment methods with different positions
    When the administrator adds a new payment method with a higher position than existing ones
    Then the system adds the new payment method to the end of the list
    And the payment methods remain sorted in ascending order by position

Scenario: Add new payment method to the beginning of the list
    Given there are multiple payment methods with different positions
    When the administrator adds a new payment method with a lower position than existing ones
    Then the system adds the new payment method to the beginning of the list
    And the payment methods remain sorted in ascending order by position

Scenario: Change the position of an existing payment method
    Given there are multiple payment methods with different positions
    When the administrator updates the position of an existing payment method to a lower value
    Then the system updates the position of the payment method
    And the payment methods remain sorted in ascending order by position
