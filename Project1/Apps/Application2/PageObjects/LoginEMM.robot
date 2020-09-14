*** Settings ***
Documentation  All page object related to Welcome page fo CS360

Library  SeleniumLibrary

# Framework Libraries
Resource  ../../../../Tool_RobotFramework/RobotLibraries/Commonkeywords.Robot

# EMM pages



*** Variables ***

#Objects



*** Keywords ***


#Object Actions
Open CS360 Application
    [Documentation]
    go to  ${ENVIRONMENT['CS360_URL']}


Fill "Username" Field
    [Documentation]
    [Arguments]  ${Username}
    Input Text  ${UsernameInput_LoginPage}  ${Username}

Fill "Password" Field
    [Documentation]
    [Arguments]  ${Password}
    input password  ${PasswordInput_LoginPage}  ${Password}

Click "Login" Button
    [Documentation]
    Click Button    ${LoginButton_LoginPage}

#Keywords
Verify Login page Loaded
    [Documentation]    CS360 >> Welcome page >> Verify page Loaded
    ...                Author              :       Niket Shinde
    Wait Until Page Contains    Welcome to Tieto Smart Utilities.  timeout=${TIMEOUT_WAIT}






