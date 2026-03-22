Feature: browsing_inventory_story_processado

Scenario: Browsing only tracked product variants in the store
    Tags: ['@ui']
    When  I want to browse inventory
    Then  I should see only one tracked variant in the list



Scenario: Being informed about on hand quantity of a product variant
    Tags: ['@ui']
    When  I want to browse inventory
    Then  I should see that the "Iron Maiden T-Shirt" variant has 5 quantity on hand


