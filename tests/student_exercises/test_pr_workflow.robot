*** Settings ***
Documentation     Test exercise to verify PR workflow and CI feedback.
Library           Browser
Resource          ../../resources/common.resource
Resource          ../../resources/login_page.resource

Suite Setup       Open SauceDemo
Suite Teardown    Close SauceDemo

*** Test Cases ***
Verify Login Page Title
    [Documentation]    Check that the SauceDemo login page has the correct title.
    [Tags]    student    exercise    ci-test
    Get Title    ==    Swag Labs

Verify Login Button Exists
    [Documentation]    Check that the login button is present on the page.
    [Tags]    student    exercise    ci-test
    Get Element Count    id=login-button    ==    1
