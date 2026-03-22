Feature: apply_story_processado

Scenario: Apply for a job with valid information
    Given there is a job opening with the title "Software Engineer"
    And the user has a valid profile with personal information
    When the user applies for the job "Software Engineer"
    And provides valid application information
    Then the system accepts the job application
    And displays a confirmation message

Scenario: Apply for a non-existent job
    Given there is no job opening with the title "Non Existent Job"
    When the user applies for the job "Non Existent Job"
    And provides valid application information
    Then the system denies the job application
    And displays a message indicating that the job is not available

Scenario: Apply for a job with missing information
    Given there is a job opening with the title "Software Engineer"
    And the user has a valid profile with personal information
    When the user applies for the job "Software Engineer"
    And provides incomplete application information
    Then the system denies the job application
    And displays a message indicating the required fields

Scenario: Apply for a job without a valid profile
    Given there is a job opening with the title "Software Engineer"
    And the user does not have a valid profile with personal information
    When the user attempts to apply for the job "Software Engineer"
    Then the system prompts the user to complete their profile
    And does not allow the job application

Scenario: Multiple job applications for the same position
    Given there is a job opening with the title "Software Engineer"
    And the user has a valid profile with personal information
    And the user has already applied for the job "Software Engineer"
    When the user attempts to apply again for the job "Software Engineer"
    Then the system denies the duplicate job application
    And displays a message indicating that the user has already applied
