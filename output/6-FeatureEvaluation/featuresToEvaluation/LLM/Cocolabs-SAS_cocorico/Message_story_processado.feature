Feature: Message_story_processado

Scenario: Send a message to an offerer
    Given there is a user "asker@example.com" who wants to send a message
    And there is an offerer "offerer@example.com" with a listed item
    When the user "asker@example.com" sends a message to "offerer@example.com"
    Then the system records the message
    And the offerer "offerer@example.com" receives the message

Scenario: Consult received messages
    Given there is an offerer "offerer@example.com" with received messages
    When the offerer "offerer@example.com" consults their messages
    Then the system displays a list of received messages
    And the list includes the sender's information and the message content

Scenario: Reply to a received message
    Given there is an offerer "offerer@example.com" with a received message from "asker@example.com"
    When the offerer "offerer@example.com" replies to the message
    Then the system records the reply
    And the asker "asker@example.com" receives the reply

Scenario: Consult sent messages
    Given there is a user "asker@example.com" who has sent messages
    When the user "asker@example.com" consults their sent messages
    Then the system displays a list of sent messages
    And the list includes the recipient's information and the message content

Scenario: Attempt to send a message to a non-existent user
    Given there is no user with the email "nonexistent@example.com"
    When a user sends a message to "nonexistent@example.com"
    Then the system denies sending the message
    And displays a message indicating that the recipient does not exist
