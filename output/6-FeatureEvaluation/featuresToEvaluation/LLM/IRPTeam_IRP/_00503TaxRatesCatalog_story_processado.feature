Feature: _00503TaxRatesCatalog_story_processado

Scenario: Create a new tax rate with valid information
    Given there is an administrator logged in
    And the tax rates catalog is empty
    When the administrator creates a new tax rate with the code "VAT" and rate "20"
    And adds a multilingual description for the tax rate "VAT" in English as "Value Added Tax"
    Then the system saves the new tax rate
    And displays a confirmation message

Scenario: Attempt to create a tax rate with duplicate code
    Given there is an administrator logged in
    And there is a tax rate with the code "VAT" and rate "20"
    When the administrator creates a new tax rate with the code "VAT" and rate "15"
    Then the system denies the creation
    And displays an error message indicating that the tax rate code already exists

Scenario: Create a tax rate with invalid rate value
    Given there is an administrator logged in
    And the tax rates catalog is empty
    When the administrator creates a new tax rate with the code "VAT" and rate "abc"
    Then the system denies the creation
    And displays an error message indicating that the tax rate value is invalid

Scenario: Update an existing tax rate
    Given there is an administrator logged in
    And there is a tax rate with the code "VAT" and rate "20"
    When the administrator updates the tax rate "VAT" with a new rate "25"
    Then the system saves the updated tax rate
    And displays a confirmation message

Scenario: Delete a tax rate
    Given there is an administrator logged in
    And there is a tax rate with the code "VAT" and rate "20"
    When the administrator deletes the tax rate "VAT"
    Then the system removes the tax rate
    And displays a confirmation message indicating that the tax rate has been deleted
