Feature: product_review_validation_1_story_processado

Scenario: Add product review with missing title
    Given the Administrator is managing product reviews
    And there is a product review without a title
    When the Administrator attempts to add the product review
    Then the system prevents the addition of the review
    And displays a message indicating that the title is required

Scenario: Add product review with missing comment
    Given the Administrator is managing product reviews
    And there is a product review with a title but without a comment
    When the Administrator attempts to add the product review
    Then the system prevents the addition of the review
    And displays a message indicating that the comment is required

Scenario: Add product review with both title and comment
    Given the Administrator is managing product reviews
    And there is a product review with a title and a comment
    When the Administrator attempts to add the product review
    Then the system allows the addition of the review
    And displays a message confirming successful addition

Scenario: Add product review with missing both title and comment
    Given the Administrator is managing product reviews
    And there is a product review without a title and without a comment
    When the Administrator attempts to add the product review
    Then the system prevents the addition of the review
    And displays a message indicating that both title and comment are required

Scenario: Cancel adding product review
    Given the Administrator is managing product reviews
    And there is a product review with some details entered
    When the Administrator cancels adding the product review
    Then the system discards the review details
    And returns to the product review management page
