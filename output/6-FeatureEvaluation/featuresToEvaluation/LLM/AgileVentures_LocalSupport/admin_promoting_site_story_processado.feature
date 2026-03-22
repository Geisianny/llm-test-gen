Feature: admin_promoting_site_story_processado

Scenario: Site name is displayed on the homepage
    Given the user is on the homepage
    Then the site name "Harrow Community Network" is displayed prominently
    And the site's visual identity is visible

Scenario: Site name is displayed on internal pages
    Given the user is on an internal page
    Then the site name "Harrow Community Network" is displayed prominently
    And the site's visual identity is visible

Scenario: Site name is displayed consistently across different pages
    Given the user navigates through different pages
    Then the site name "Harrow Community Network" is displayed consistently
    And the site's visual identity remains the same

Scenario: Site name is displayed with correct branding
    Given the user is on any page of the site
    Then the site name "Harrow Community Network" is displayed with the correct branding
    And the site's visual identity matches the brand guidelines

Scenario: Site name is visible on page load
    Given the user loads a page on the site
    Then the site name "Harrow Community Network" is visible on page load
    And there are no delays in displaying the site name
