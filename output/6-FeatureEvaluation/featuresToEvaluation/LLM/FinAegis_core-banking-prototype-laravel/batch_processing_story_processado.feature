Feature: batch_processing_story_processado

Scenario: Create a new asset basket successfully
    Given the system administrator is logged in
    And there are existing assets in the system
    When the administrator creates a new asset basket with valid assets
    Then the system creates the asset basket
    And displays a confirmation message

Scenario: Attempt to create an asset basket with invalid assets
    Given the system administrator is logged in
    And there are existing assets in the system
    When the administrator creates a new asset basket with invalid assets
    Then the system denies the creation of the asset basket
    And displays an error message indicating the invalid assets

Scenario: Decompose an existing asset basket
    Given the system administrator is logged in
    And there is an existing asset basket
    When the administrator decomposes the asset basket
    Then the system decomposes the asset basket
    And displays a confirmation message

Scenario: Attempt to decompose a non-existent asset basket
    Given the system administrator is logged in
    And there is no asset basket with the specified ID
    When the administrator attempts to decompose the non-existent asset basket
    Then the system denies the decomposition
    And displays an error message indicating that the asset basket does not exist

Scenario: Rebalance an existing asset basket
    Given the system administrator is logged in
    And there is an existing asset basket with assets
    When the administrator rebalances the asset basket
    Then the system rebalances the asset basket
    And displays a confirmation message indicating the new composition
