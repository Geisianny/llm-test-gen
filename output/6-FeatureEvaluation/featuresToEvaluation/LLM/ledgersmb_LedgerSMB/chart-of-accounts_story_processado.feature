Feature: chart-of-accounts_story_processado

Scenario: View chart of accounts
    Given the user is logged into LedgerSMB
    And the chart of accounts is populated with accounts and headings
    When the user navigates to the chart of accounts page
    Then the system displays the chart of accounts
    And includes all accounts and headings with their respective details

Scenario: Modify account properties
    Given the user is logged into LedgerSMB
    And there is an existing account with specific properties
    When the user edits the account properties
    And changes the account description to "New Account Description"
    Then the system updates the account properties
    And displays the updated account description "New Account Description"

Scenario: Modify heading properties
    Given the user is logged into LedgerSMB
    And there is an existing heading with specific properties
    When the user edits the heading properties
    And changes the heading description to "New Heading Description"
    Then the system updates the heading properties
    And displays the updated heading description "New Heading Description"

Scenario: Create new account based on existing account
    Given the user is logged into LedgerSMB
    And there is an existing account with specific properties
    When the user creates a new account based on the existing account
    And modifies the new account's description to "New Account Based on Existing"
    Then the system creates the new account
    And displays the new account with the description "New Account Based on Existing"

Scenario: Attempt to create duplicate account
    Given the user is logged into LedgerSMB
    And there is an existing account with a unique account number
    When the user creates a new account with the same account number as the existing account
    Then the system prevents the creation of the new account
    And displays an error message indicating that the account number is already in use
