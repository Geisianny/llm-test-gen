Feature: index_13_story_processado

Scenario: Navigation
    Given  the current page is the provider dashboard
    When  they select "Audience" from the context selector
    And  they follow "Subscriptions" within the main menu's section Accounts
    Then  the current page is the provider service subscriptions page



Scenario: Empty view
    Given  the provider has no service subscriptions
    When  they go to the provider service subscriptions page
    Then  they should see an empty state



Scenario: Empty search
    Given  a buyer "Mouse"
    And  the buyer is subscribed to product "Elephant Taming"
    When  they go to the provider service subscriptions page
    And  the table is filtered with:
    Then  they should see an empty search state



Scenario: Filter subscriptions by product
    Given  a buyer "Mouse"
    And  the buyer is subscribed to product "Elephant Taming"
    And  the buyer is subscribed to product "Zeebra Stripe Drawing"
    When  they go to the provider service subscriptions page
    And  the table should contain the following:
    When  the table is filtered with:
    And  the table should contain the following:



Scenario: Filter subscriptions by account
    Tags: ['@search']
    Given  a buyer "Ben"
    And  the buyer is subscribed to product "My API"
    And  a buyer "Bender"
    And  the buyer is subscribed to product "My API"
    And  a buyer "Leela"
    And  the buyer is subscribed to product "My API"
    When  they go to the provider service subscriptions page
    And  the table is filtered with:
    Then  the table should contain the following:



Scenario: Filter subscriptions by service plan
    Given  the following service plans:
    And  the following buyers with service subscriptions signed up to the provider:
    When  they go to the provider service subscriptions page
    And  the table is filtered with:
    Then  the table should contain the following:



Scenario: Filter subscriptions by state
    Given  a buyer "Bender"
    And  the buyer is subscribed to product "Elephant Taming"
    And  a buyer "Leela"
    And  the buyer is subscribed to product "Zeebra Stripe Drawing"
    When  they go to the provider service subscriptions page
    And  the table is filtered with:
    Then  they should see an empty search state
    When  the table is filtered with:
    Then  the table should contain the following:



Scenario: Filter paid subscriptions
    Tags: ['@wip']
    Given  the following service plans:
    And  the following buyers with service subscriptions signed up to the provider:
    When  they go to the provider service subscriptions page
    And  the table is filtered with:
    Then  the table should contain the following:



Scenario: Ordering and filtering by service
    Given  the following service plan:
    Given  a buyer "First"
    And  a buyer "Second"
    And  buyer "First" is subscribed to plan "Service Plan"
    And  buyer "Second" is subscribed to plan "Service Plan"
    And  buyer "First" plan "Service Plan" contract gets suspended
    When  they go to the provider service subscriptions page
    When  the table is filtered with:
    And  the table is sorted by "State"
    And  the table should contain the following:



Scenario: Order by plan name
    Tags: ['@wip']
    Given  a buyer "Someone"
    And  the following service plans:
    And  the following buyers with service subscriptions signed up to the provider:
    When  they go to the buyer's service subscriptions page
    Then  the table should contain the following:
    And  the table is sorted by "Plan"
    Then  the table should contain the following:



Scenario: Outline 11: Ordering - Example 1
    When  they go to the provider service subscriptions page
    And  the table is sorted by "Account"
    Then  the table should be sorted by "Account"



