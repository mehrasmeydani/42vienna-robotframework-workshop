*** Settings ***
Documentation     Keywords for interacting with the SauceDemo shopping cart page.
Library           Browser

*** Variables ***
${CART_ITEMS}             css=.cart_item
${CHECKOUT_BUTTON}        id=checkout
${CONTINUE_SHOPPING}      id=continue-shopping
${CART_ITEM_NAME}         css=.inventory_item_name

*** Keywords ***
Open Cart
    [Documentation]    Navigate to the shopping cart page.
    Click    css=.shopping_cart_link

Cart Should Contain
    [Documentation]    Verify that a product with the given name is in the cart.
    [Arguments]    ${product_name}
    Get Element Count    css=.cart_item:has-text("${product_name}")    >=    1

Cart Should Be Empty
    [Documentation]    Verify that the cart contains no items.
    ${items}=    Get Elements    ${CART_ITEMS}
    ${count}=    Get Length    ${items}
    Should Be Equal As Numbers    ${count}    0

Remove Item From Cart
    [Documentation]    Click the Remove button for a product in the cart by its name.
    [Arguments]    ${product_name}
    Click    css=.cart_item:has-text("${product_name}") button[id^="remove"]

Proceed To Checkout
    [Documentation]    Click the Checkout button on the cart page.
    Click    ${CHECKOUT_BUTTON}

Continue Shopping
    [Documentation]    Click the Continue Shopping button to return to the products page.
    Click    ${CONTINUE_SHOPPING}
