Feature: _00505CurrencyMovementType_story_processado

Scenario: Create a new currency movement type with valid information
    Given there is an administrator logged into the system
    And there are no existing currency movement types with the name "TRY Partner Terms"
    When the administrator creates a new currency movement type with the name "TRY Partner Terms"
    And configures it for the Turkish Lira (TRY) currency
    And links it to the "European Central Bank" exchange rate source
    Then the system saves the new currency movement type
    And displays a confirmation message indicating successful creation

Scenario: Attempt to create a duplicate currency movement type
    Given there is an administrator logged into the system
    And there is an existing currency movement type with the name "TRY Partner Terms"
    When the administrator creates a new currency movement type with the name "TRY Partner Terms"
    And configures it for the Turkish Lira (TRY) currency
    And links it to the "European Central Bank" exchange rate source
    Then the system prevents the creation of the duplicate currency movement type
    And displays an error message indicating that a currency movement type with the same name already exists

Scenario: Update an existing currency movement type
    Given there is an administrator logged into the system
    And there is an existing currency movement type with the name "TRY Partner Terms"
    When the administrator updates the currency movement type with the name "TRY Partner Terms"
    And changes its linked exchange rate source to "Bloomberg"
    Then the system saves the updated currency movement type
    And displays a confirmation message indicating successful update

Scenario: Delete an existing currency movement type
    Given there is an administrator logged into the system
    And there is an existing currency movement type with the name "TRY Partner Terms"
    When the administrator deletes the currency movement type with the name "TRY Partner Terms"
    Then the system removes the currency movement type
    And displays a confirmation message indicating successful deletion

Scenario: Attempt to delete a non-existent currency movement type
    Given there is an administrator logged into the system
    And there is no existing currency movement type with the name "Non Existent"
    When the administrator attempts to delete the currency movement type with the name "Non Existent"
    Then the system prevents the deletion
    And displays an error message indicating that the currency movement type does not exist
