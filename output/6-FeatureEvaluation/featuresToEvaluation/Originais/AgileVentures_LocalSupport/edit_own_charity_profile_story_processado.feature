Feature: edit_own_charity_profile_story_processado

Scenario: Successfully add website url without protocol
    Tags: ['@vcr']
    Given  I am signed in as a charity worker related to "Friendly"
    And  I update "Friendly" charity website to be "www.friendly.com"
    Then  the website link for "Friendly" should have a protocol



Scenario: Successfully change the address of a charity
    Tags: ['@vcr']
    Given  I am signed in as a charity worker related to "Friendly"
    And  I update "Friendly" charity address to be "30 pinner road"
    Then  I should be on the show page for the organisation named "Friendly"



Scenario: Do not see edit button as non-superadmin not associated with Friendly
    Given  I am signed in as a charity worker unrelated to "Friendly"
    And  I visit the show page for the organisation named "Friendly"
    Then  I should not see an edit button for "Friendly" charity



Scenario: Non-logged in users do not see edit button either
    Given  I visit the show page for the organisation named "Friendly"
    Then  I should not see an edit button for "Friendly" charity



Scenario: Change the address of a charity when Google is indisposed
    Tags: ['@vcr']
    Given  I am signed in as a charity worker related to "Friendly"
    And  I update "Friendly" charity address to be "83 pinner road" when Google is indisposed
    Then  I should not see the unable to save organisation error
    Then  the address for "Friendly" should be "83 pinner road"
    And  I visit the show page for the organisation named "Friendly"



Scenario: Redirected to sign-in when not signed-in and edit donation url
    Given  I visit the edit page for the organisation named "Friendly"
    Then  I should be on the sign in page



Scenario: By default, not display organisations address and phone number on home page
    Given  I visit the show page for the organisation named "Friendly"
    Then  I should not see any address or telephone information for "Nice" and "Friendly"



Scenario: By default, not display organisations edit and delete on home page
    Given  I visit the show page for the organisation named "Friendly"
    Then  I should not see any edit or delete links



Scenario: By default, not display organisations address and phone number on details page
    Given  I visit the show page for the organisation named "Friendly"
    Then  I should not see any address or telephone information for "Friendly"



Scenario: By default, not display edit link on details page
    Given  I visit the show page for the organisation named "Friendly"
    Then  I should not see any edit link for "Friendly"



Scenario: Outline 11: Successfully mark a field of a charity as public or private - Example 1
    Tags: ['@vcr']
    Given  I am signed in as a charity worker related to "Friendly"
    And  I visit the edit page for the organisation named "Friendly"
    And  the phone for "Friendly" has been marked hidden
    And  I check "organisation_publish_phone"
    And  I press "Update Organisation"
    Then  I should be on the show page for the organisation named "Friendly"
    And  I should see "020800000"
    And  I should see "Telephone"




Scenario: Outline 12: Edit page has scroll box for selecting categories - Example 1
    Given  I am signed in as a charity worker related to "Friendly"
    And  I visit the edit page for the organisation named "Friendly"
    Then  I should see the category named Animal welfare as the 1st category in What you do




Scenario: Outline 13: Appropriate categories are checked/unchecked by default - Example 1
    Given  I am signed in as a charity worker related to "Friendly"
    And  I visit the edit page for the organisation named "Friendly"
    Then  the category named Health should be checked




Scenario: Outline 14: Successfully add and remove an organisation's categories - Example 1
    Tags: ['@vcr']
    Given  I am signed in as a charity worker related to "Friendly"
    And  I visit the edit page for the organisation named "Friendly"
    Then  I uncheck the category "Health"
    And  I check the category "Child welfare"
    And  I press "Update Organisation"
    Then  I should not see "Health" within "org-categories"
    And  I should see "Child welfare" within "org-categories"



