Feature: search_elastic_story_processado

Scenario: Search for a valid term
    Given the site visitor is on a site using the SearchElastic search engine
    And the Elasticsearch index contains relevant results for the term "hubble"
    When the site visitor performs a search for "hubble"
    Then the system displays a list of relevant search results
    And the results are retrieved directly from the Elasticsearch index

Scenario: Search for an invalid term
    Given the site visitor is on a site using the SearchElastic search engine
    And the Elasticsearch index does not contain relevant results for the term " invalidterm"
    When the site visitor performs a search for "invalidterm"
    Then the system displays a message indicating no results were found
    And the message suggests alternatives or provides guidance on refining the search

Scenario: Search with empty query
    Given the site visitor is on a site using the SearchElastic search engine
    When the site visitor performs a search with an empty query
    Then the system displays a message indicating the query is empty
    And the message requests the user to enter a valid search term

Scenario: Search with special characters
    Given the site visitor is on a site using the SearchElastic search engine
    When the site visitor performs a search with special characters "!@#$"
    Then the system handles the special characters correctly
    And displays a message indicating no results were found or provides relevant results if available

Scenario: Search with multiple terms
    Given the site visitor is on a site using the SearchElastic search engine
    And the Elasticsearch index contains relevant results for the terms "space exploration"
    When the site visitor performs a search for "space exploration"
    Then the system displays a list of relevant search results
    And the results are relevant to both "space" and "exploration" terms
