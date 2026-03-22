Feature: in-arrears-purchase_story_processado

Scenario: COGS posting when purchasing parts in arrears (still short)
    Given  10 units sold
    When  5 units are purchased at 10 USD each
    Then  the inventory should be at 0 USD
    And  COGS should be at 50 USD



Scenario: COGS posting when purchasing parts in arrears (exact match)
    Given  10 units sold
    When  10 units are purchased at 10 USD each
    Then  the inventory should be at 0 USD
    And  COGS should be at 100 USD



Scenario: COGS posting when purchasing parts in arrears (partly into inventory)
    Given  10 units sold
    When  20 units are purchased at 10 USD each
    Then  the inventory should be at 100 USD
    And  COGS should be at 100 USD


