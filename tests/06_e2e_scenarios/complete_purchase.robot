*** Settings ***
Documentation     End-to-end test: complete purchase flow from login to order confirmation.
...               This is the "crown jewel" test that ties everything together.
...               It uses all resource files and demonstrates a real-world scenario.
Library           Browser
Resource          ../../resources/saucedemo.resource

Suite Setup       Open SauceDemo
Suite Teardown    Close SauceDemo

*** Test Cases ***
Complete Purchase Of Single Item
    [Documentation]    Login → add product → checkout → verify order confirmation.
    # Step 1: Login
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Login Should Succeed

    # Step 2: Add a product to the cart
    Add Product To Cart    Sauce Labs Backpack
    Cart Badge Should Show    1

    # Step 3: Go to cart and proceed to checkout
    Open Cart
    Cart Should Contain    Sauce Labs Backpack
    Proceed To Checkout

    # Step 4: Fill checkout information
    Fill Checkout Information    Jane    Smith    10001

    # Step 5: Verify overview and complete
    Get Text    css=.title    ==    Checkout: Overview
    Complete Checkout

    # Step 6: Verify order confirmation
    Order Should Be Confirmed

Complete Purchase Of Multiple Items
    [Documentation]    Login → add multiple products → checkout → verify confirmation.
    Go To    ${BASE_URL}
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Login Should Succeed

    # Add two products
    Add Product To Cart    Sauce Labs Bike Light
    Add Product To Cart    Sauce Labs Bolt T-Shirt
    Cart Badge Should Show    2

    # Checkout
    Open Cart
    Cart Should Contain    Sauce Labs Bike Light
    Cart Should Contain    Sauce Labs Bolt T-Shirt
    Proceed To Checkout
    Fill Checkout Information    Test    User    99999
    Complete Checkout

    # Verify
    Order Should Be Confirmed
