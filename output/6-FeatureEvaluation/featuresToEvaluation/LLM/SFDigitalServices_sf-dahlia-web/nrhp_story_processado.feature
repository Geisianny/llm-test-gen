Feature: nrhp_story_processado

Scenario: Claim NRHP with valid address
    Given there is an applicant with a valid address within the NRHP area
    When the applicant fills out the short form application
    And enters a valid address within the NRHP area
    Then the system allows the applicant to claim "Live in the Neighborhood"
    And displays a field to upload supporting documents

Scenario: Claim NRHP with invalid address
    Given there is an applicant with an address outside the NRHP area
    When the applicant fills out the short form application
    And enters an address outside the NRHP area
    Then the system does not allow the applicant to claim "Live in the Neighborhood"
    And displays a message indicating that the address is not within the NRHP area

Scenario: Claim NRHP with eligible household members
    Given there is an applicant with household members having valid addresses within the NRHP area
    When the applicant fills out the short form application
    And selects eligible household members residing within the NRHP area
    Then the system allows the applicant to claim "Live in the Neighborhood" for the selected household members
    And displays a field to upload supporting documents for the selected household members

Scenario: Upload supporting documents for NRHP claim
    Given there is an applicant who has claimed "Live in the Neighborhood" with a valid address
    When the applicant uploads supporting documents for the NRHP claim
    Then the system accepts the uploaded documents
    And displays a confirmation that the NRHP claim has been successfully submitted

Scenario: Claim NRHP with missing supporting documents
    Given there is an applicant who has claimed "Live in the Neighborhood" with a valid address
    When the applicant submits the application without uploading supporting documents
    Then the system displays a message requesting the upload of supporting documents
    And does not finalize the NRHP claim until the documents are uploaded
