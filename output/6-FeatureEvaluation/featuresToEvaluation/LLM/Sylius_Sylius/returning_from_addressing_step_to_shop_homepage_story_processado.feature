Feature: returning_from_addressing_step_to_shop_homepage_story_processado

Scenario: Return to shop homepage from checkout addressing step
    Given there is a visitor with items in the cart
    And the visitor is at the checkout addressing step
    When the visitor clicks on the link to return to the shop homepage
    Then the visitor is redirected to the shop homepage
    And the cart items are preserved

Scenario: Cart contents remain after returning to shop homepage
    Given there is a visitor with items in the cart
    And the visitor is at the checkout addressing step
    When the visitor clicks on the link to return to the shop homepage
    Then the cart still contains the items
    And the visitor can continue shopping

Scenario: Visitor can navigate back to checkout
    Given there is a visitor with items in the cart
    And the visitor is at the checkout addressing step
    When the visitor clicks on the link to return to the shop homepage
    And the visitor navigates back to checkout
    Then the visitor is returned to the checkout addressing step

Scenario: Return to shop homepage with empty cart
    Given there is a visitor with an empty cart
    And the visitor is at the checkout addressing step
    When the visitor clicks on the link to return to the shop homepage
    Then the visitor is redirected to the shop homepage
    And the cart remains empty

Scenario: Multiple attempts to return to shop homepage
    Given there is a visitor with items in the cart
    And the visitor is at the checkout addressing step
    When the visitor clicks on the link to return to the shop homepage
    And the visitor navigates back to checkout
    And the visitor clicks on the link to return to the shop homepage again
    Then the visitor is redirected to the shop homepage
    And the cart items are preserved
