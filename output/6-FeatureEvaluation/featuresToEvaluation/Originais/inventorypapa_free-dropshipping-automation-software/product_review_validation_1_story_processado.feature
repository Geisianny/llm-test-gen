Feature: product_review_validation_1_story_processado

Scenario: Trying to remove title from an existing product review
    Tags: ['@ui', '@api']
    When  I want to modify the "Awesome" product review
    And  I remove its title
    And  I try to save my changes
    Then  I should be notified that title is required
    And  this product review should still be titled "Awesome"



Scenario: Trying to remove comment from an existing product review
    Tags: ['@ui', '@api']
    When  I want to modify the "Awesome" product review
    And  I remove its comment
    And  I try to save my changes
    Then  I should be notified that comment is required
    And  this product review should still have a comment "Nice product"


