Feature: 0032-PRIM-025_story_processado

Scenario: Persistent order results in an auction (one trigger breached), no orders placed during auction,
    And  the market data for the market "BTC/ETH" should be:
    Given  the parties place the following orders:
    When  the network moves ahead "1" blocks
    Then  the trading mode should be "TRADING_MODE_MONITORING_AUCTION" for the market "BTC/ETH"
    And  the orders should have the following states:
    When  the network moves ahead "1" blocks
    Then  the trading mode should be "TRADING_MODE_CONTINUOUS" for the market "BTC/ETH"
    And  the mark price should be "1050" for the market "BTC/ETH"
    And  the orders should have the following states:
    And  the market data for the market "BTC/ETH" should be:


