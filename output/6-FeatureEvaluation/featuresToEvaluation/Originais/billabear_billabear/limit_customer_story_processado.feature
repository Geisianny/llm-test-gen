Feature: limit_customer_story_processado

Scenario: Get customer info
    Given  I have authenticated to the API
    And  the follow customers exist:
    And  the following subscriptions exist:
    When  I request the limits for customer "customer.one@example.org"
    Then  I should see that "Feature Two" is limited to 25



Scenario: Disabled
    Given  I have authenticated to the API
    And  the follow customers exist:
    And  the following subscriptions exist:
    And  customer "customer.one@example.org" is disabled
    When  I request the limits for customer "customer.one@example.org"
    Then  I should see an empty limits API response


