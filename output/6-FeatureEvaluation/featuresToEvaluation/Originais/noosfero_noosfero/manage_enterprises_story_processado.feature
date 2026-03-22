Feature: manage_enterprises_story_processado

Scenario: seeing my enterprises on menu
    Tags: ['@selenium']
    Given  I am logged in as "joaosilva"
    And  I follow "menu-dropdown"
    Then  I should see "My enterprises" link
    When  I follow "My enterprises"
    Then  I should see "Manage Tangerine Dream" link
    And  I follow "Manage Tangerine Dream"
    Then  I should be on tangerine-dream's control panel



Scenario: not show enterprises on menu to a user without enterprises
    Tags: ['@selenium']
    Given  I am logged in as "mariasilva"
    And  I follow "menu-dropdown"
    Then  I should not see "My enterprises" link


