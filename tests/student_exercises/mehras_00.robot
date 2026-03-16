*** Settings ***
Documentation     Mehra's Exercise 00 - Basic Login and Cart Interaction
...               This test verifies that a user can log in and add/remove items from the cart through products pages.
Library           Browser
Resource		  ../../resources/saucedemo.resource

Suite Setup       Open SauceDemo
Suite Teardown    Close SauceDemo

*** Test Cases ***
User Is Able To Log In And ADD/REMOVE Items
    [Documentation]    error_user should be able to log in.

    Login With Credentials    error_user    ${VALID_PASSWORD}
    Login Should Succeed

    FOR    ${product}    IN    @{PRODUCT_LIST}
		Add Product To Cart    ${product}
		Cart Badge Should Show    1
		Remove Product From Cart    ${product}
		Cart Badge Should Show    0
    END
    Go To    ${BASE_URL}

*** Keywords ***
# This section is empty here because we import keywords from resources.
# You could define test-specific keywords here if needed.
