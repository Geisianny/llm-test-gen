Feature: login_story_processado

Scenario: Redirecting / to /login.pl
    When  I navigate to the application root
    Then  I should see the application login page



Scenario: Viewing setup.pl
    When  I navigate to the setup login page
    Then  I should see the setup login page



Scenario: Viewing login.pl
    When  I navigate to the application login page
    Then  I should see the application login page


