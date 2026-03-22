Feature: returning_from_addressing_step_to_shop_homepage_story_processado

Scenario: Returning to shop from addressing step
    Tags: ['@no-api', '@ui']
    When  I added product "The Stick of Truth" to the cart
    And  I am at the checkout addressing step
    When  I go back to store
    Then  I should be redirected to the homepage


