Feature: min_config_state_channel_story_processado

Scenario: Create a new state channel
    Given there are no existing state channels with the name "Test Channel"
    When the user creates a new state channel named "Test Channel"
    Then the system creates the state channel "Test Channel"
    And the state channel "Test Channel" is listed in the available state channels

Scenario: Associate a system with a state channel
    Given there is an existing state channel named "Test Channel"
    And there is a registered system named "Test System"
    When the user associates the system "Test System" with the state channel "Test Channel"
    Then the system "Test System" is associated with the state channel "Test Channel"
    And the state channel "Test Channel" is listed in the system's associated channels

Scenario: Apply a state channel to a system
    Given there is an existing state channel named "Test Channel" with a valid configuration
    And there is a registered system named "Test System" associated with the state channel "Test Channel"
    When the user applies the state channel "Test Channel" to the system "Test System"
    Then the system applies the configuration from the state channel "Test Channel"
    And the system "Test System" reports a successful configuration application

Scenario: Delete the only revision of a state channel
    Given there is an existing state channel named "Test Channel" with a single revision
    When the user attempts to delete the only revision of the state channel "Test Channel"
    Then the system prevents the deletion of the only revision
    And displays a message indicating that at least one revision must exist

Scenario: Remove a system from a state channel
    Given there is an existing state channel named "Test Channel"
    And there is a registered system named "Test System" associated with the state channel "Test Channel"
    When the user removes the system "Test System" from the state channel "Test Channel"
    Then the system "Test System" is no longer associated with the state channel "Test Channel"
    And the state channel "Test Channel" is not listed in the system's associated channels
