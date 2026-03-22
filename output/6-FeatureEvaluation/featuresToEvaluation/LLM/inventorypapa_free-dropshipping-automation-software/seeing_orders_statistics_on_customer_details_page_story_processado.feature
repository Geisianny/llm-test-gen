Feature: seeing_orders_statistics_on_customer_details_page_story_processado

Scenario: View customer order statistics with multiple orders
    Given there is a customer with multiple orders placed across different sales channels
    And the customer has orders with varying fulfillment statuses
    When the administrator views the customer's details page
    Then the system displays the total number of orders placed by the customer
    And the total value of all orders

Scenario: View customer order statistics with no orders
    Given there is a customer with no orders placed
    When the administrator views the customer's details page
    Then the system displays zero as the total number of orders
    And zero as the total value of all orders

Scenario: View customer order statistics with orders across different sales channels
    Given there is a customer with orders placed across multiple sales channels
    When the administrator views the customer's details page
    Then the system displays order statistics segmented by sales channel
    And the total value of orders for each sales channel

Scenario: View customer order statistics with different fulfillment statuses
    Given there is a customer with orders having different fulfillment statuses
    When the administrator views the customer's details page
    Then the system displays order statistics segmented by fulfillment status
    And the total value of orders for each fulfillment status

Scenario: View customer order statistics with average order value
    Given there is a customer with multiple orders placed
    When the administrator views the customer's details page
    Then the system displays the average value of the customer's orders
    And the total number of orders and total value are also displayed
