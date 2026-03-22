Feature: governance_voting_story_processado

Scenario: Create a new proposal with valid details
    Given there is a stakeholder with tokens staked
    When the stakeholder creates a new proposal with a valid title and description
    Then the system creates the proposal
    And displays a message confirming successful proposal creation

Scenario: Vote on an existing proposal with sufficient voting power
    Given there is a stakeholder with tokens staked and a proposal exists
    When the stakeholder votes on the existing proposal
    Then the system records the vote
    And updates the proposal's voting results

Scenario: Vote on an existing proposal without sufficient voting power
    Given there is a stakeholder without tokens staked and a proposal exists
    When the stakeholder votes on the existing proposal
    Then the system denies the vote
    And displays a message indicating insufficient voting power

Scenario: Execute an approved proposal
    Given there is an approved proposal and the voting period has ended
    When the system executes the approved proposal
    Then the proposal is implemented
    And the system displays a message confirming successful execution

Scenario: Delegate voting power to another stakeholder
    Given there is a stakeholder with tokens staked
    When the stakeholder delegates voting power to another stakeholder
    Then the system updates the voting power of the delegate
    And displays a message confirming successful delegation
