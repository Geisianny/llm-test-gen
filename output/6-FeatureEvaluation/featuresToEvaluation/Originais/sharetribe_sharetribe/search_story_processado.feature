Feature: search_story_processado

Scenario: basic search
    Tags: ['@javascript']
    When  I fill in "q" with "sofa"
    And  I press "search-button"
    Then  I should see "old sofa for sale"



Scenario: should exclude non-matching results
    Tags: ['@javascript']
    When  I fill in "q" with "chair"
    And  I press "search-button"
    Then  I should not see "old sofa for sale"
    And  I should see "Sorry, no listings could be found for your search criteria"



Scenario: Finding by description
    Tags: ['@javascript']
    When  I fill in "q" with "pink"
    And  I press "search-button"
    Then  I should see "old sofa for sale"



Scenario: Finding by partial word
    Tags: ['@javascript']
    When  I fill in "q" with "wond"
    And  I press "search-button"
    Then  I should see "old sofa for sale"
    When  I fill in "q" with "ofa"
    And  I press "search-button"
    Then  I should see "old sofa for sale"



Scenario: Finding by numeric field (and search term)
    Tags: ['@javascript']
    When  I set search range for numeric filter "Weight (kg)" between "10" and "200"
    And  I press "Update view"
    Then  I should see "old sofa for sale"
    Then  I should see "light-weigth plastic outdoor sofa"
    When  I set search range for numeric filter "Weight (kg)" between "100" and "200"
    And  I press "Update view"
    Then  I should see "old sofa for sale"
    Then  I should not see "light-weigth plastic outdoor sofa"
    When  I fill in "q" with "light-weight"
    And  I press "search-button"
    Then  I should see "Sorry, no listings could be found for your search criteria"



Scenario: Finding by price
    Tags: ['@javascript']
    When  I set price range between "100" and "1000"
    And  I press "Update view"
    Then  I should see "old sofa for sale"
    Then  I should not see "light-weigth plastic outdoor sofa"
    When  I set price range between "500" and "1000"
    And  I press "Update view"
    Then  I should see "Sorry, no listings could be found for your search criteria"



Scenario: Finding by checkbox field
    Tags: ['@javascript']
    When  I check "3 people"
    And  I press "Update view"
    Then  I should see "old sofa for sale"
    Then  I should see "light-weigth plastic outdoor sofa"
    When  I check "Outdoors"
    And  I press "Update view"
    Then  I should not see "old sofa for sale"
    Then  I should see "light-weigth plastic outdoor sofa"
    When  I check "Indoors"
    And  I press "Update view"
    Then  I should not see "old sofa for sale"
    Then  I should not see "light-weigth plastic outdoor sofa"


