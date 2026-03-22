Feature: _00509PaymentTermsCatalog_story_processado

Scenario: _005024 filling in the "Payment terms" catalog
    When  set True value to the constant
    *  Opening a form and creating Payment terms
    Given  I open hyperlink "e1cib/list/Catalog.PaymentSchedules"
    When  create a catalog element with the name Test
    *  Check for created Payment terms
    Then  I check for the "PaymentSchedules" catalog element with the "Description_en" "Test ENG"
    Then  I check for the "PaymentSchedules" catalog element with the "Description_tr" "Test TR"


