Feature: country_condition_2_story_processado

Scenario: Add a new country category price rule which is valid
    Given  adding a product price rule named "country-discount"
    And  the price rule is active
    And  the price rule has a condition countries with country "Austria"
    Then  the price rule should be valid for product "Shoe"
    Then  the price rule should be valid for product "Shoe 2"



Scenario: Add a new country category price rule which is invalid
    Given  the site has a country "Germany" with currency "EUR"
    Given  adding a product price rule named "country-discount"
    And  the price rule is active
    And  the price rule has a condition countries with country "Germany"
    Then  the price rule should be invalid for product "Shoe"
    Then  the price rule should be invalid for product "Shoe 2"


