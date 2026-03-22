Feature: admin_services_story_processado

Scenario: Managing services
    Given  a logged in admin user
    And  I am on the admin dashboard
    And  there are no services
    When  I follow "Services"
    Then  I should see "No services have been added yet"
    When  I follow "Add a New Service"
    And  I fill in "Name" with "Java"
    And  I check "service[checked]"
    And  I press "Save"
    Then  I should see "Java"
    When  I follow "Edit"
    And  I fill in "Name" with "Ruby on Rails"
    And  I press "Save"
    Then  I should see "Ruby on Rails"
    When  I follow "Delete"
    Then  I should not see "Ruby on Rails"


