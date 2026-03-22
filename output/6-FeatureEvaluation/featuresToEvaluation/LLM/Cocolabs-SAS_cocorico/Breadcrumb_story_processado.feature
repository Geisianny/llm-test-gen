Feature: Breadcrumb_story_processado

Scenario: Verify breadcrumbs for Messages under Offerer menu
    Given the user is on the homepage
    And the user navigates to the "Offerer" menu
    When the user clicks on "Messages"
    Then the breadcrumbs display "Home > Offerer > Messages"

Scenario: Verify breadcrumbs for a direct child page
    Given the user is on the homepage
    When the user navigates to "Offerer"
    Then the breadcrumbs display "Home > Offerer"

Scenario: Verify breadcrumbs for the homepage
    Given the user is on the homepage
    Then the breadcrumbs display "Home"

Scenario: Verify breadcrumbs after navigating through multiple levels
    Given the user is on the homepage
    And the user navigates to "Offerer"
    And the user clicks on "Messages"
    When the user clicks on "Home" in the breadcrumbs
    Then the breadcrumbs display "Home"

Scenario: Verify breadcrumbs remain consistent on page reload
    Given the user is on the "Messages" page under "Offerer"
    And the breadcrumbs display "Home > Offerer > Messages"
    When the user reloads the page
    Then the breadcrumbs still display "Home > Offerer > Messages"
