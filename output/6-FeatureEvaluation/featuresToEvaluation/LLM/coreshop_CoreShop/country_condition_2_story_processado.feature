Feature: country_condition_2_story_processado

Scenario: Create a new product with a valid price rule for the configured country
    Given there is an active price rule for the country "USA"
    And there is a category "Electronics"
    When the user creates a new product "Smartphone" associated with the category "Electronics"
    And configures the product for the country "USA"
    Then the system considers the product valid
    And applies the price rule for the country "USA"

Scenario: Create a new product with an invalid price rule for a different country
    Given there is an active price rule for the country "USA"
    And there is a category "Electronics"
    When the user creates a new product "Smartphone" associated with the category "Electronics"
    And configures the product for the country "Canada"
    Then the system considers the product invalid
    And does not apply the price rule for the country "USA"

Scenario: Create a new product without an associated category
    Given there is no category "Toys"
    When the user creates a new product "Toy Car" without an associated category
    Then the system considers the product invalid
    And displays a message indicating that a category is required

Scenario: Create a new product with multiple categories
    Given there is a category "Electronics"
    And there is a category "Gadgets"
    When the user creates a new product "Smartwatch" associated with the categories "Electronics" and "Gadgets"
    And configures the product for the country "USA"
    Then the system considers the product valid
    And applies the price rule for the country "USA"

Scenario: Create a new product when there are no active price rules
    Given there are no active price rules
    And there is a category "Electronics"
    When the user creates a new product "Smartphone" associated with the category "Electronics"
    And configures the product for the country "USA"
    Then the system considers the product valid
    And displays a message indicating that no price rules are applied
