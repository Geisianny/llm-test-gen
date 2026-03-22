Feature: 0026-AUCT-029_story_processado

Scenario: A market with default trading mode "continuous trading" will start with an opening auction. The opening auction will
              there are orders crossing on the book, there is no need for the supplied liquidity to exceed a threshold to exit an auction: (0026-AUCT-029)
    And  the parties place the following orders:
    When  the network moves ahead "50" blocks
    Then  the trading mode should be "TRADING_MODE_OPENING_AUCTION" for the market "BTC/ETH"
    When  the network moves ahead "52" blocks
    Then  the trading mode should be "TRADING_MODE_CONTINUOUS" for the market "BTC/ETH"



Scenario: No crossed orders, no leaving the auction
    And  the parties place the following orders:
    When  the network moves ahead "102" blocks
    Then  the trading mode should be "TRADING_MODE_OPENING_AUCTION" for the market "BTC/ETH"


