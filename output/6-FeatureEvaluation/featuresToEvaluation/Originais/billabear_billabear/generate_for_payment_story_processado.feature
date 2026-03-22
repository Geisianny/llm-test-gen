Feature: generate_for_payment_story_processado

Scenario: Get customer info
    When  I have logged in as "sally.brown@example.org" with the password "AF@k3P@ss"
    And  the follow customers exist:
    And  the following subscriptions exist:
    And  there is a payments for:
    When  I generate a receipt for the payment for "customer.one@example.org" for 3500
    Then  then there will be a receipt for "customer.one@example.org" for 3500


