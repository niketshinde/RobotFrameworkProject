*** Settings ***
Documentation  All Keywords related to EMM Application

# Framework Libraries
Resource  ../../../Tool_RobotFramework/RobotLibraries/Commonkeywords.Robot


# EMM Pages
Resource  PageObjects/LoginEMM.robot

*** Variables ***



*** Keywords ***

Login
    [Documentation]    Login To CS360
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}  ${Username}=${ENVIRONMENT['CS360_USERNAME']}  ${Password}=${ENVIRONMENT['CS360_PASSWORD']}
    Commonkeywords.Keyword Setup  ${ITR}


    [Teardown]  Commonkeywords.Keyword Teardown  ${ITR}
