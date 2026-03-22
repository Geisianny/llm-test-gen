Feature: _0296Unbundling_story_processado

Scenario: _029600 preparation (Unbundling)
    When  set True value to the constant
    *  Load info
    When  Create catalog ItemKeys objects
    When  Create catalog ItemTypes objects
    When  Create catalog Units objects
    When  Create catalog Items objects
    When  Create catalog Specifications objects
    When  Create chart of characteristic types AddAttributeAndProperty objects
    When  Create catalog AddAttributeAndPropertySets objects
    When  Create catalog AddAttributeAndPropertyValues objects
    When  Create catalog Companies objects (Main company)
    When  Create catalog PriceTypes objects
    When  Create catalog Currencies objects
    When  Create catalog Partners objects (Ferron BP)
    When  Create catalog Companies objects (partners company)
    When  Create catalog Countries objects
    When  Create information register PartnerSegments records
    When  Create catalog PartnerSegments objects
    When  Create catalog Agreements objects
    When  Create chart of characteristic types CurrencyMovementType objects
    When  Create catalog TaxRates objects
    When  Create catalog Taxes objects
    When  Create information register TaxSettings records
    When  Create catalog IntegrationSettings objects
    When  Create information register CurrencyRates records
    When  Create information register Taxes records (VAT)



Scenario: _0296001 check preparation
    When  check preparation



Scenario: _029601 create Unbundling on a product with a specification (specification created in advance, Store does not use Shipment confirmation and Goods receipt)
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    *  Create Unbundling for Dress/A-8, all item keys were created in advance
    And  I click the button named "FormCreate"
    And  I click Select button of "Company" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item key bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Choice button of the field named "Unit"
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I input "2,000" text in the field named "Quantity"
    And  I click Select button of "Store" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I move to "Item list" tab
    And  in the table "ItemList" I click "By specification" button
    And  I click the button named "FormPost"
    And  I delete "$$NumberUnbundling0029601$$" variable
    And  I delete "$$Unbundling0029601$$" variable
    And  I save the value of "Number" field as "$$NumberUnbundling0029601$$"
    And  I save the window as "$$Unbundling0029601$$"
    And  I click the button named "FormPostAndClose"
    *  Check the creation of Unbundling
    And  "List" table contains lines
    And  I close all client application windows



Scenario: _029604 create Unbundling on a product with a specification (specification created in advance, Store use Shipment confirmation and Goods receipt)
    When  create a purchase invoice for the purchase of sets and dimensional grids at the tore 02
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    *  Create Unbundling for Boots/S-8, all item keys were created in advance
    And  I click the button named "FormCreate"
    And  I click Select button of "Company" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item key bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Choice button of the field named "Unit"
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I input "2,000" text in the field named "Quantity"
    And  I click Select button of "Store" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I move to "Item list" tab
    And  in the table "ItemList" I click "By specification" button
    And  I click the button named "FormPost"
    And  I delete "$$NumberUnbundling0029604$$" variable
    And  I delete "$$Unbundling0029604$$" variable
    And  I save the value of "Number" field as "$$NumberUnbundling0029604$$"
    And  I save the window as "$$Unbundling0029604$$"
    And  I click the button named "FormPostAndClose"
    *  Check the creation of Unbundling
    And  "List" table contains lines
    And  I close all client application windows



Scenario: _029610 create Unbundling (+check movements) for bundl which was created independently
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    *  Create Unbundling for Bundle Dress+Shirt
    And  I click the button named "FormCreate"
    And  I click Select button of "Company" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item key bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Choice button of the field named "Unit"
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I input "2,000" text in the field named "Quantity"
    And  I click Select button of "Store" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I move to "Item list" tab
    And  in the table "ItemList" I click "By specification" button
    And  I click the button named "FormPost"
    And  I delete "$$NumberUnbundling0029610$$" variable
    And  I delete "$$Unbundling0029610$$" variable
    And  I save the value of "Number" field as "$$NumberUnbundling0029610$$"
    And  I save the window as "$$Unbundling0029610$$"
    And  I click the button named "FormPostAndClose"
    *  Check the creation of Unbundling
    And  "List" table contains lines
    And  I close all client application windows



Scenario: _029611 create Unbundling (+check movements) for bundl (there is a Bundling document) for which the specification was changed
    *  Change specification Dress+Trousers
    Given  I open hyperlink "e1cib/list/Catalog.Specifications"
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I activate field named "Quantity*" in "FormTable*" table
    And  I input "4,000" text in "Quantity" field of "FormTable*" table
    And  I finish line editing in "FormTable*" table
    And  I click "Save and close" button
    And  Delay 5
    *  Create Unbundling for item Dress+Trousers
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    And  I click the button named "FormCreate"
    And  I click Select button of "Company" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item key bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Choice button of the field named "Unit"
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I input "2,000" text in the field named "Quantity"
    And  I click Select button of "Store" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I move to "Item list" tab
    And  in the table "ItemList" I click "By bundle content" button
    And  "ItemList" table contains lines
    And  I click the button named "FormPost"
    And  I delete "$$NumberUnbundling0029611$$" variable
    And  I delete "$$Unbundling0029611$$" variable
    And  I save the value of "Number" field as "$$NumberUnbundling0029611$$"
    And  I save the window as "$$Unbundling0029611$$"
    And  I click the button named "FormPostAndClose"
    *  Check the creation of Unbundling
    And  "List" table contains lines
    And  I close all client application windows



Scenario: _029612 create Unbundling
    *  Opening the creation form Unbundling
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    And  I click the button named "FormCreate"
    *  Filling in details
    And  I click Select button of "Company" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Select button of "Item key bundle" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I click Choice button of the field named "Unit"
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I input "2,000" text in the field named "Quantity"
    And  I click Select button of "Store" field
    And  I go to line in "List" table
    And  I select current line in "List" table
    And  I move to "Item list" tab
    And  in the table "ItemList" I click "By specification" button
    *  Post unbundling
    And  I click the button named "FormPost"
    And  I delete "$$NumberUnbundling0029612$$" variable
    And  I delete "$$Unbundling0029612$$" variable
    And  I save the value of "Number" field as "$$NumberUnbundling0029612$$"
    And  I save the window as "$$Unbundling0029612$$"
    And  I close all client application windows
    *  Check creation
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    And  "List" table contains lines
    And  I close all client application windows



Scenario: _300520 check connection to Unbundling report "Related documents"
    Given  I open hyperlink "e1cib/list/Document.Unbundling"
    *  Form report Related documents
    And  I go to line in "List" table
    And  I click the button named "FormFilterCriterionRelatedDocumentsRelatedDocuments"
    And  Delay 1
    Then  "* Related documents" window is opened
    And  I close all client application windows


