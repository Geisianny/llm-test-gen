Feature: edit_donation_info_story_processado

Scenario: Successfully change the donation url for a charity
    Tags: ['@vcr']
    Given  I visit the home page
    And  I sign in as "registered_user@example.com" with password "pppppppp"
    Given  I visit the edit page for the organisation named "Friendly"
    And  I edit the donation url to be "http://www.friendly.com/donate"
    And  I press "Update Organisation"
    Then  I should be on the show page for the organisation named "Friendly"
    And  I should see "Organisation was successfully updated"
    And  the donation_info URL for "Friendly" should refer to "http://www.friendly.com/donate"


