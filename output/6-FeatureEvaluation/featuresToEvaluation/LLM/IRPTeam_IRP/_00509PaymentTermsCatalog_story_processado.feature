Feature: _00509PaymentTermsCatalog_story_processado

Scenario: Create a new payment term with a custom name
    Given there is an administrator logged into the system
    And the payment terms catalog is empty
    When the administrator creates a new payment term named "Custom Term"
    Then the system saves the new payment term
    And displays a confirmation message

Scenario: Create a new payment term with multilingual descriptions
    Given there is an administrator logged into the system
    And the payment terms catalog is empty
    When the administrator creates a new payment term with the description "English Description" in English
    And adds a description "French Description" in French
    Then the system saves the new payment term with multilingual descriptions
    And displays a confirmation message

Scenario: Edit an existing payment term
    Given there is an administrator logged into the system
    And there is a payment term named "Existing Term" in the catalog
    When the administrator edits the payment term "Existing Term"
    And changes its name to "Updated Term"
    Then the system updates the payment term
    And displays a confirmation message

Scenario: Attempt to create a duplicate payment term
    Given there is an administrator logged into the system
    And there is a payment term named "Existing Term" in the catalog
    When the administrator creates a new payment term with the name "Existing Term"
    Then the system prevents the creation of the duplicate payment term
    And displays an error message indicating that the term already exists

Scenario: Delete a payment term
    Given there is an administrator logged into the system
    And there is a payment term named "Term to Delete" in the catalog
    When the administrator deletes the payment term "Term to Delete"
    Then the system removes the payment term from the catalog
    And displays a confirmation message
