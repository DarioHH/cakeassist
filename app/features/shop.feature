# Created by Dario at 24/02/2019
# this module check the cr5eation and load  the shop information

Feature: # Show how load to the order
  # Enter feature description her

  Scenario: # Chooose the local
    Given I login in the system
    And I choose the shop
    Then Should see the available cakes.


  Scenario: Create the order
    Given I am in the list of cakes
    And should be in the list the cakes
    |name |
    | rsapberry mouse|
    |chocotorta      |
    | alternativa    |
    | uruguaya       |
    And I choose 3 cakes "chocotorta"
    And I choose 2 cakes "uruguaaya"
    Then I press to button with the name resume
    Then I should see the windows with the datails of the order
    Then I press to button "confifm"
    Then I should be a message with the status of operation