Feature: pay_invoice_story_processado

Scenario: Make payments in different currency with the pay invoice wizard
    Tags: ['@bug511104', '@bug496889', '@bug497078']
    Given  I have recorded on the 1 jan 2009 an invoice (in_invoice) of 1000,0 CHF without tax called MySupplierInvoicePayWizard
    When  I press the validate button
    Then  I should see the invoice MySupplierInvoicePayWizard open
    When  I call the Pay invoice wizard
    And  I partially pay 200.0 CHF.- on the 10 jan 2009
    Then  I should see a residual amount of 800.0 CHF.-
    When  I call the Pay invoice wizard
    And  I partially pay 200.0 USD.- on the 11 jan 2009
    Then  I should see a residual amount of 561.48 CHF.-
    When  I call the Pay invoice wizard
    And  I partially pay 200.0 EUR.- on the 12 jan 2009
    Then  I should see a residual amount of 232.68 CHF.-
    When  I call the Pay invoice wizard
    And  I completely pay the residual amount in CHF on the 13 sep 2009
    Then  I should see a residual amount of 0.0 CHF.-
    And  I should see the invoice MySupplierInvoicePayWizard paid


