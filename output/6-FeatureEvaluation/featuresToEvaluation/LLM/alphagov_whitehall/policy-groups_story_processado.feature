Feature: policy-groups_story_processado

Scenario: Create a new Policy Group
    Given there is no existing Policy Group with the title "Climate Change Experts"
    When the editor creates a new Policy Group with the title "Climate Change Experts"
    And enters the summary "Experts on climate change policies"
    And enters the description "Detailed description of climate change experts"
    And enters the contact email "climatechange@example.com"
    And uploads an attachment "climatechange.pdf"
    Then the system creates the Policy Group
    And displays a confirmation message

Scenario: Associate multiple Policy Groups with a single policy
    Given there is a policy with the title "New Environmental Policy"
    And there are two Policy Groups with titles "Climate Change Experts" and "Renewable Energy Advocates"
    When the editor associates the Policy Groups "Climate Change Experts" and "Renewable Energy Advocates" with the policy "New Environmental Policy"
    Then the system displays the metadata on the policy page
    And the metadata reads "Groups: Climate Change Experts, Renewable Energy Advocates"

Scenario: Display Policy Group metadata on policy page
    Given there is a policy with the title "New Environmental Policy"
    And there is a Policy Group with the title "Climate Change Experts"
    When the editor associates the Policy Group "Climate Change Experts" with the policy "New Environmental Policy"
    Then the system displays the metadata on the policy page
    And the metadata reads "Groups: Climate Change Experts"

Scenario: View Policy Group page with contents list
    Given there is a Policy Group with the title "Climate Change Experts"
    And the description contains headings "Summary", "Key Experts", and "Methodology"
    When the citizen views the Policy Group page
    Then the system displays the title "Climate Change Experts"
    And displays a contents list with anchor links to "Summary", "Key Experts", and "Methodology"

Scenario: Access Policy Group profile from policy page
    Given there is a policy with the title "New Environmental Policy"
    And there is a Policy Group with the title "Climate Change Experts"
    And the Policy Group is associated with the policy "New Environmental Policy"
    When the citizen clicks on the link "Climate Change Experts" on the policy page
    Then the system navigates to the Policy Group page
    And displays the title "Climate Change Experts"
