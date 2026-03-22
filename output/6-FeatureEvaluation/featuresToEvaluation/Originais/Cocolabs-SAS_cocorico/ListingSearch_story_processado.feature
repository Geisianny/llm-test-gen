Feature: ListingSearch_story_processado

Scenario: I can find listings by location, categories, characteristics, date and price
    Given  I do a search on the home page
    Then  I should be on the "listing search result" page
    And  I should see "1 results"
    When  I fill date range with the following:
    And  I drag range slider ".range-box .ui-slider" with min equal to "40" and max equal to "400"
    And  I select a characteristic "Characteristic_3" with value "Custom value 1"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "listing search result" page
    And  I should see "1 results"



Scenario: I can not find listings without searched categories
    Given  I do a search on the home page
    Then  I should be on the "listing search result" page
    And  I should see "1 results"
    When  I select categories "Category2_2"
    And  I select a characteristic "Characteristic_3" with value "Custom value 1"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "listing search result" page
    And  I should see "0 results"



Scenario: I can not find listings without searched characteristics
    Given  I do a search on the home page
    Then  I should be on the "listing search result" page
    And  I should see "1 results"
    When  I select a characteristic "Characteristic_3" with value "Custom value 2"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "listing search result" page
    And  I should see "0 results"



Scenario: I can not find listings unavailable
    Given  I do a search on the home page
    Then  I should be on the "listing search result" page
    And  I should see "1 results"
    When  I fill date range with the following:
    And  I select a characteristic "Characteristic_3" with value "Custom value 1"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "listing search result" page
    And  I should see "0 results"



Scenario: I cannot find listings with price out of searched price range
    Given  I do a search on the home page
    Then  I should be on the "listing search result" page
    And  I should see "1 results"
    When  I fill date range with the following:
    And  I drag range slider ".range-box .ui-slider" with min equal to "150" and max equal to "300"
    And  I select a characteristic "Characteristic_3" with value "Custom value 1"
    And  I wait 500 ms for Jquery loading
    Then  I should be on the "listing search result" page
    And  I should see "0 results"


