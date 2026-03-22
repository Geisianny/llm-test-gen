Feature: NetworkFlow_story_processado

Scenario: Add a custom network via popular network flow
    Given the user is on the network settings page
    And there is a list of popular networks available
    When the user selects a popular network to add
    Then the system adds the selected network
    And displays a confirmation message

Scenario: Add a custom network via custom network flow
    Given the user is on the network settings page
    When the user chooses to add a custom network
    And enters the network details: name "Custom Network", RPC URL "https://customnetwork.com", Chain ID "123", and symbol "CN"
    Then the system adds the custom network
    And displays a confirmation message

Scenario: Attempt to add a custom network with invalid RPC URL
    Given the user is on the network settings page
    When the user chooses to add a custom network
    And enters the network details: name "Invalid Network", RPC URL "invalidurl", Chain ID "123", and symbol "IN"
    Then the system denies adding the custom network
    And displays an error message indicating that the RPC URL is invalid

Scenario: Remove a previously added custom network
    Given the user is on the network settings page
    And there is a custom network "Custom Network" already added
    When the user chooses to remove the custom network "Custom Network"
    Then the system removes the custom network
    And displays a confirmation message

Scenario: Attempt to add a duplicate custom network
    Given the user is on the network settings page
    And there is a custom network "Custom Network" already added
    When the user chooses to add a custom network
    And enters the network details: name "Custom Network", RPC URL "https://customnetwork.com", Chain ID "123", and symbol "CN"
    Then the system denies adding the custom network
    And displays an error message indicating that the network already exists
