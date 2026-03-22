Feature: edit_block_of_links_story_processado

Scenario: Edit link block with valid link and icon
    Given there is a profile owner with a link block on their site
    When the profile owner edits the link block with the title "Social Media"
    And enters the link "https://www.example.com/socialmedia"
    And selects the icon "facebook"
    Then the system saves the changes
    And displays the updated link block with the selected icon

Scenario: Edit link block with invalid link
    Given there is a profile owner with a link block on their site
    When the profile owner edits the link block with the title "Invalid Link"
    And enters the invalid link "not a url"
    Then the system displays an error message
    And does not save the changes

Scenario: Edit link block without icon selection
    Given there is a profile owner with a link block on their site
    When the profile owner edits the link block with the title "No Icon"
    And enters the link "https://www.example.com/noicon"
    Then the system saves the changes
    And displays the updated link block without an icon

Scenario: Edit link block with empty link
    Given there is a profile owner with a link block on their site
    When the profile owner edits the link block with the title "Empty Link"
    And clears the link field
    Then the system displays an error message
    And does not save the changes

Scenario: Cancel editing link block
    Given there is a profile owner with a link block on their site
    When the profile owner edits the link block with the title "Cancel Edit"
    And enters the link "https://www.example.com/cancel"
    And cancels the editing process
    Then the system does not save the changes
    And displays the original link block unchanged
