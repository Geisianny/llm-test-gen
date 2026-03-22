Feature: index_13_story_processado

Scenario: View list of customer service subscriptions
    Given there are customer service subscriptions for a provider
    When the provider navigates to the subscriptions page
    Then the system displays a list of customer service subscriptions
    And the list includes the status, plan, billing type, value, and service for each subscription

Scenario: Search customer service subscriptions by account
    Given there are customer service subscriptions for a provider
    When the provider searches for subscriptions by account name "Example Account"
    Then the system displays a list of customer service subscriptions for "Example Account"
    And the list includes the status, plan, billing type, value, and service for each subscription

Scenario: Filter customer service subscriptions by status
    Given there are customer service subscriptions with different statuses for a provider
    When the provider filters subscriptions by status "Active"
    Then the system displays a list of customer service subscriptions with "Active" status
    And the list includes the plan, billing type, value, and service for each subscription

Scenario: Display empty state for no search results
    Given there are no customer service subscriptions matching the search criteria "Non-existent Account"
    When the provider searches for subscriptions by account name "Non-existent Account"
    Then the system displays a message indicating no subscriptions were found
    And the message suggests checking the search criteria

Scenario: Filter customer service subscriptions by multiple criteria
    Given there are customer service subscriptions with different attributes for a provider
    When the provider filters subscriptions by service "API Service" and plan "Premium"
    Then the system displays a list of customer service subscriptions for "API Service" with "Premium" plan
    And the list includes the status, billing type, and value for each subscription
