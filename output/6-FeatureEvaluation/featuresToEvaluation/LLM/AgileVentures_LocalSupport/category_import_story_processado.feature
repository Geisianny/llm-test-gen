Feature: category_import_story_processado

Scenario: Import categories from a valid CSV file
    Given there is a Site Super Admin user logged in
    And there is a CSV file containing valid categories
    When the Super Admin imports the CSV file
    Then the system imports the categories successfully
    And the categories are added to the system

Scenario: Associate imported categories with existing organisations
    Given there is a Site Super Admin user logged in
    And there are existing organisations in the system
    And there is a CSV file containing valid categories
    When the Super Admin imports the CSV file
    Then the system allows associating the imported categories with the existing organisations

Scenario: Import categories from an invalid CSV file
    Given there is a Site Super Admin user logged in
    And there is a CSV file with invalid format or data
    When the Super Admin imports the CSV file
    Then the system displays an error message
    And the categories are not added to the system

Scenario: Import categories with duplicate names
    Given there is a Site Super Admin user logged in
    And there is a CSV file containing categories with names that already exist in the system
    When the Super Admin imports the CSV file
    Then the system displays a message indicating that duplicate categories exist
    And the duplicate categories are not added to the system

Scenario: Import categories from an empty CSV file
    Given there is a Site Super Admin user logged in
    And there is an empty CSV file
    When the Super Admin imports the CSV file
    Then the system displays a message indicating that the file is empty
    And no categories are added to the system
