Feature: confirm_email_story_processado

Scenario: User confirms correct code
    Given  an unconfirmed user "ExistingUser" with the password "RealPassword" and the confirmation code "random-code" exists
    When  I confirm the code "random-code"
    Then  the user "ExistingUser" will be confirmed



Scenario: User confirms correct code
    Given  an unconfirmed user "ExistingUser" with the password "RealPassword" and the confirmation code "random-code" exists
    When  I confirm the code "random-code-two"
    Then  the user "ExistingUser" will not be confirmed


