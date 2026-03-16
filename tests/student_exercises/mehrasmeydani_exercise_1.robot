*** Settings ***
Documentation     Cart add and remove tests for standard_user and error_user.
...               Verifies that items added to the cart can also be removed,
...               and that error_user can add items to the cart.
Library           Browser
Resource          ../../resources/common.resource
Resource          ../../resources/login_page.resource
Resource          ../../resources/products_page.resource
Resource          ../../resources/cart_page.resource

Suite Setup       Open SauceDemo
Suite Teardown    Close SauceDemo

*** Variables ***
${PRODUCT}    Sauce Labs Backpack

*** Keywords ***
Login As Standard User
    [Documentation]    Navigate to SauceDemo and log in as standard_user.
    Go To    ${BASE_URL}
    Login With Credentials    standard_user    secret_sauce
    Login Should Succeed

Login As Error User
    [Documentation]    Navigate to SauceDemo and log in as error_user.
    Go To    ${BASE_URL}
    Login With Credentials    error_user    secret_sauce
    Login Should Succeed

*** Test Cases ***
Standard User Can Add Item To Cart
    [Documentation]    Add a product to the cart and verify it appears there.
    [Tags]    student    exercise
    Login As Standard User
    Add Product To Cart    ${PRODUCT}
    Cart Badge Should Show    1
    Open Cart
    Cart Should Contain    ${PRODUCT}

Standard User Can Remove Item From Cart
    [Documentation]    Add a product to the cart, then remove it and verify the cart is empty.
    [Tags]    student    exercise
    Login As Standard User
    Add Product To Cart    ${PRODUCT}
    Open Cart
    Cart Should Contain    ${PRODUCT}
    Remove Item From Cart    ${PRODUCT}
    Cart Should Be Empty

Error User Can Add Item To Cart
    [Documentation]    Log in as error_user (a user that returns errors on some actions) and verify
    ...                that adding a product to the cart still works and the item appears in the cart.
    [Tags]    student    exercise
    Login As Error User
    Add Product To Cart    ${PRODUCT}
    Open Cart
    Cart Should Contain    ${PRODUCT}
