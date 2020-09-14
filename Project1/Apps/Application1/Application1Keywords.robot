*** Settings ***
Documentation  All Keywords related to CS360 Application

# Framework Libraries
Resource  ../../../Tool_RobotFramework/RobotLibraries/Commonkeywords.Robot


# CS360 Pages
Resource  PageObjects/LoginCS360.robot
Resource  PageObjects/WelcomeCS360.robot
Resource  PageObjects/PersonCustomerOverviewCS360.robot
Resource  PageObjects/CustomerAgreementsCS360.robot

*** Variables ***



*** Keywords ***

Login
    [Documentation]    Login To CS360
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}  ${Username}=${ENVIRONMENT['CS360_USERNAME']}  ${Password}=${ENVIRONMENT['CS360_PASSWORD']}
    Commonkeywords.Keyword Setup  ${ITR}

    LoginCS360.Login To CS360 With valid Creadentials  ${Username}    ${Password}
    WelcomeCS360.Verify Welcome page Loaded
    WelcomeCS360.Validate Welcome page Contents

    [Teardown]  Commonkeywords.Keyword Teardown  ${ITR}
