*** Settings ***
Documentation     Checkout flow tests for SauceDemo.
...               Covers filling checkout information and form validation.
Library           Browser
Resource          ../../resources/common.resource
Resource          ../../resources/login_page.resource
Resource          ../../resources/products_page.resource
Resource          ../../resources/cart_page.resource
Resource          ../../resources/checkout_page.resource

Suite Setup       Login And Add Item To Cart
Suite Teardown    Close SauceDemo

*** Keywords ***
Login And Add Item To Cart
    Open SauceDemo
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Login Should Succeed
    Add Product To Cart    Sauce Labs Backpack

*** Test Cases ***
Checkout With Valid Information
    [Documentation]    Complete checkout with valid first name, last name, and zip code.
    Open Cart
    Proceed To Checkout
    Fill Checkout Information    John    Doe    12345
    # Should be on the checkout overview page
    Get Text    css=.title    ==    Checkout: Overview
    # Go back to continue testing
    Go To    ${BASE_URL}/inventory.html

Checkout With Missing First Name Should Fail
    [Documentation]    Checkout should fail if first name is empty.
    Open Cart
    Proceed To Checkout
    Fill Checkout Information    ${EMPTY}    Doe    12345
    Get Text    css=.error-message-container    contains    First Name is required
    Go To    ${BASE_URL}/inventory.html

Checkout With Missing Last Name Should Fail
    [Documentation]    Checkout should fail if last name is empty.
    Open Cart
    Proceed To Checkout
    Fill Checkout Information    John    ${EMPTY}    12345
    Get Text    css=.error-message-container    contains    Last Name is required
    Go To    ${BASE_URL}/inventory.html

Checkout With Missing Postal Code Should Fail
    [Documentation]    Checkout should fail if postal code is empty.
    Open Cart
    Proceed To Checkout
    Fill Checkout Information    John    Doe    ${EMPTY}
    Get Text    css=.error-message-container    contains    Postal Code is required
    Go To    ${BASE_URL}/inventory.html
