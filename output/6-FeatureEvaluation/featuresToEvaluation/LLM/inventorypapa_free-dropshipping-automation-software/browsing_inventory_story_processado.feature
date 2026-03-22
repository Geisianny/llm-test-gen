Feature: browsing_inventory_story_processado

Scenario: Browse tracked product variants
    Given there are tracked product variants in the inventory
    When the administrator accesses the inventory browser
    Then the system displays a list of tracked product variants
    And shows the available stock quantity for each variant

Scenario: Filter tracked product variants
    Given there are tracked product variants in the inventory
    When the administrator accesses the inventory browser
    And filters for monitored items only
    Then the system displays a list of monitored tracked product variants
    And shows the available stock quantity for each variant

Scenario: Browse tracked product variants with no items
    Given there are no tracked product variants in the inventory
    When the administrator accesses the inventory browser
    Then the system displays a message indicating that there are no tracked product variants

Scenario: Browse tracked product variants with pagination
    Given there are multiple pages of tracked product variants in the inventory
    When the administrator accesses the inventory browser
    Then the system displays a list of tracked product variants with pagination
    And shows the available stock quantity for each variant on the first page

Scenario: View detailed information of a tracked product variant
    Given there is a tracked product variant in the inventory
    When the administrator selects the tracked product variant
    Then the system displays detailed information about the tracked product variant
    And includes the available stock quantity
