Feature: SendEthGasApiDown_story_processado

Scenario: Send ETH when Gas API is down with valid transaction details
    Given the Gas API is unavailable
    And the user has a valid ETH balance
    And the user has entered valid recipient address and amount
    When the user initiates an ETH send transaction
    Then the system uses fallback gas properties for the transaction
    And the transaction is processed successfully

Scenario: Send ETH when Gas API is down with insufficient balance
    Given the Gas API is unavailable
    And the user has an insufficient ETH balance for the transaction
    And the user has entered valid recipient address and amount
    When the user initiates an ETH send transaction
    Then the system displays an error message indicating insufficient balance
    And the transaction is not processed

Scenario: Send ETH when Gas API is down with invalid recipient address
    Given the Gas API is unavailable
    And the user has a valid ETH balance
    And the user has entered an invalid recipient address
    When the user initiates an ETH send transaction
    Then the system displays an error message indicating invalid recipient address
    And the transaction is not processed

Scenario: Send ETH when Gas API is down and then becomes available
    Given the Gas API is unavailable
    And the user has a valid ETH balance
    And the user has entered valid recipient address and amount
    When the user initiates an ETH send transaction
    And the Gas API becomes available during the transaction process
    Then the system completes the transaction using the fallback gas properties initially
    And the transaction is processed successfully

Scenario: Cancel Send ETH transaction when Gas API is down
    Given the Gas API is unavailable
    And the user has a valid ETH balance
    And the user has initiated an ETH send transaction
    When the user cancels the transaction
    Then the system cancels the transaction successfully
    And the user's ETH balance remains unchanged
