Feature: edit_block_of_links_story_processado

Scenario: show the icon selector
    Tags: ['@selenium-fixme']
    Given  I follow "Edit sideboxes"
    And  I follow "Edit" within ".button-bar"
    When  I follow "New link"
    Then  the "css=div.icon-selector" should not be visible
    When  I click "div.icon"
    Then  the "css=div.icon-selector" should be visible


