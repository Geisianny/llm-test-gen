Feature: bulk_affiliate_styles_upload_story_processado

Scenario: Upload a valid file within the size limit
    Given there is an admin user logged in
    And a valid file containing affiliate site styles with a size of 3 MB
    When the admin uploads the file
    Then the system processes the file
    And displays a confirmation message

Scenario: Upload a file exceeding the size limit
    Given there is an admin user logged in
    And a file containing affiliate site styles with a size of 5 MB
    When the admin uploads the file
    Then the system denies the upload
    And displays an error message indicating that the file size exceeds the limit

Scenario: Upload an invalid file type
    Given there is an admin user logged in
    And a file of type "image/jpeg" containing affiliate site styles
    When the admin uploads the file
    Then the system denies the upload
    And displays an error message indicating that the file type is not supported

Scenario: Receive email notification after file processing
    Given there is an admin user logged in
    And a valid file containing affiliate site styles with a size of 3 MB
    When the admin uploads the file
    And the system processes the file
    Then the admin receives an email notification with the processing results

Scenario: Upload a file with incorrect formatting
    Given there is an admin user logged in
    And a file containing affiliate site styles with incorrect formatting
    When the admin uploads the file
    Then the system processes the file
    And the admin receives an email notification indicating that the file has errors
    And the email contains details about the errors found
