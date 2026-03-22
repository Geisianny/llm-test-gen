Feature: Review_story_processado

Scenario: As offerer i can add a rating to an asker
    Given  I am logged in as user "offerer@cocorico.rocks" with password "12345678"
    When  I click on dashboard menu "Comments" of "offerer"
    Then  I should be on the "dashboard reviews received" page
    And  I wait 500 ms for Jquery loading
    And  I should see "You must make notation for booking" in the "div.area" element
    When  I follow "Add your rating"
    And  I wait 500 ms for Jquery loading
    And  I click on the element with css selector "#user-rating-make a"
    And  I fill in the following:
    And  I press "Publish this comment"
    And  I wait 1000 ms
    Then  I should be on the "dashboard reviews added" page



Scenario: As asker i can add a rating to an offerer so that i can see my rating listing and user page
    Given  I am logged in as user "asker@cocorico.rocks" with password "12345678"
    When  I click on dashboard menu "Comments" of "asker"
    Then  I should be on the "dashboard reviews received" page
    And  I wait 500 ms for Jquery loading
    And  I should see "You must make notation for booking" in the "div.area" element
    And  I follow "Add your rating"
    And  I wait 500 ms for Jquery loading
    When  I click on the element with css selector "#user-rating-make a"
    And  I fill in the following:
    And  I press "Publish this comment"
    And  I wait 1000 ms
    Then  I should be on the "dashboard reviews added" page
    When  I do a search on the home page
    And  I follow "Category1_1,"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "listing show" page which "listing title" equal to "Listing One"
    When  I click on "#comments" tab
    And  I wait 2000 ms
    Then  I should see "Nice listing and offerer" in the "div.posts-holder" element
    When  I follow "OffererFirstName"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "user profile show" page which "email" equal to "offerer@cocorico.rocks"
    And  I should see "Comments (1)" in the "div.head" element
    And  I should see an ".rating" element
    And  I wait 2000 ms
    And  I should see "Nice listing and offerer" in the "div.posts-holder" element



Scenario: As user i can't add a rating without filling required fields
    Given  I am logged in as user "offerer@cocorico.rocks" with password "12345678"
    When  I click on dashboard menu "Comments" of "offerer"
    Then  I should be on the "dashboard reviews received" page
    And  I wait 500 ms for Jquery loading
    And  I should see "You must make notation for booking" in the "div.area" element
    When  I follow "Add your rating"
    And  I press "Publish this comment"
    And  I wait 2000 ms
    Then  I should see "An error has occurred." in the "div.flashes div.alert" element


