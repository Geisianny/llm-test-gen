Feature: seeing_shipping_method_when_all_units_match_to_shipping_category_story_processado

Scenario: Seeing only shipping method which category is same as categories of all my units
    Tags: ['@api', '@ui']
    Given  I added product "Rocket T-Shirt" to the cart
    And  I added product "Picasso T-Shirt" to the cart
    And  I addressed the cart
    When  I go to the shipping step
    Then  I should see "Raven Post" shipping method
    And  I should not see "Invisible Post" shipping method



Scenario: Seeing shipping method which category is same as category of my unit
    Tags: ['@api', '@ui']
    Given  I added product "Star Trek Ship" to the cart
    And  I addressed the cart
    When  I go to the shipping step
    Then  I should see "Invisible Post" shipping method
    And  I should not see "Raven Post" shipping method



Scenario: Seeing no shipping methods if my units matches to different shipping categories
    Tags: ['@api', '@ui']
    Given  I added product "Rocket T-Shirt" to the cart
    And  I added product "Star Trek Ship" to the cart
    And  I addressed the cart
    When  I go to the shipping step
    Then  there should be information about no available shipping methods



Scenario: Seeing no shipping methods if not all variants of my units has same shipping category
    Tags: ['@api', '@ui']
    Given  the "T-Shirt banana" product's "S" size belongs to "Standard" shipping category
    And  the "T-Shirt banana" product's "M" size belongs to "Over-sized" shipping category
    And  I added product "T-Shirt banana" with product option "Size" S to the cart
    And  I added product "T-Shirt banana" with product option "Size" M to the cart
    And  I addressed the cart
    When  I go to the shipping step
    Then  there should be information about no available shipping methods



Scenario: Seeing shipping methods if all variants of my units has same shipping category
    Tags: ['@api', '@ui']
    Given  the "T-Shirt banana" product's "M" size belongs to "Standard" shipping category
    And  the "T-Shirt banana" product's "S" size belongs to "Standard" shipping category
    And  I added product "T-Shirt banana" with product option "Size" S to the cart
    And  I added product "T-Shirt banana" with product option "Size" M to the cart
    And  I addressed the cart
    When  I go to the shipping step
    Then  I should see "Raven Post" shipping method
    And  I should not see "Invisible Post" shipping method


