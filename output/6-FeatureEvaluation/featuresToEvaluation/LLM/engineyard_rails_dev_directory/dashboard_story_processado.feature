Feature: dashboard_story_processado

Scenario: Provider views account overview on dashboard after login
    Given there is a registered provider with the company "ABC Solutions"
    And the provider has 5 open requests and 2 new endorsements
    When the provider logs in
    Then the dashboard displays the provider's account overview
    And includes the number of open requests and new endorsements

Scenario: Dashboard displays correct number of open requests
    Given there is a registered provider with 3 open requests
    When the provider logs in
    Then the dashboard displays 3 open requests

Scenario: Dashboard displays correct number of new endorsements
    Given there is a registered provider with 4 new endorsements
    When the provider logs in
    Then the dashboard displays 4 new endorsements

Scenario: Provider with no open requests or endorsements views dashboard
    Given there is a registered provider with no open requests or new endorsements
    When the provider logs in
    Then the dashboard displays a message indicating no open requests or new endorsements
    And the provider's account overview is still accessible

Scenario: Dashboard displays proposals associated with the provider's company
    Given there is a registered provider with the company "XYZ Inc."
    And there are 2 proposals associated with "XYZ Inc."
    When the provider logs in
    Then the dashboard displays the 2 proposals associated with "XYZ Inc."
    And includes the names of clients who have endorsed them
