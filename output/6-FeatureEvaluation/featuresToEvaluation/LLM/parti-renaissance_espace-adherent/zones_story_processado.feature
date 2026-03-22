Feature: zones_story_processado

Scenario: Access zones API as a non-logged-in user
    Given there is a non-logged-in user
    When the user requests a list of zones via the API
    Then the system returns a list of zones
    And the response is successful

Scenario: Filter zones by type via API
    Given there are zones of different types
    When the non-logged-in user requests zones of type "country" via the API
    Then the system returns a list of zones of type "country"
    And the response is successful

Scenario: Search zones by partial name via API
    Given there are zones with names containing "par"
    When the non-logged-in user searches for zones with "par" via the API
    Then the system returns a list of zones with names containing "par"
    And the response is successful

Scenario: Autocomplete zones for authenticated user within assigned area
    Given there is an authenticated user with scope to manage "city" zones
    And there are "city" zones within the user's assigned area
    When the user requests autocomplete suggestions for "city" zones with "new" via the API
    Then the system returns a list of "city" zones with names containing "new" within the user's assigned area
    And the response is successful

Scenario: Autocomplete zones for authenticated user outside assigned area
    Given there is an authenticated user with scope to manage "city" zones
    And there are "city" zones outside the user's assigned area
    When the user requests autocomplete suggestions for "city" zones with "new" via the API
    Then the system does not return "city" zones outside the user's assigned area
    And the response is successful
