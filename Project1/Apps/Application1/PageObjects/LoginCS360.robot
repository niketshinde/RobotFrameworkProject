*** Settings ***
Documentation  All page object related to Welcome page fo CS360

Library  SeleniumLibrary

# Framework Libraries
Resource  ../../../../Tool_RobotFramework/RobotLibraries/Commonkeywords.Robot

# CS360 pages
Resource  WelcomeCS360.robot


*** Variables ***

#Objects

${UsernameInput_LoginPage}  name=Username
${PasswordInput_LoginPage}  xpath=//input[@name='Password']
${LoginButton_LoginPage}  Login
${WelcomePanelH3_LoginPage}  xpath=//h3[contains(text(),'Welcome to Tieto Smart Utilities.')]


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


Login To CS360 With valid Creadentials
    [Documentation]    CS360 >> Welcome page >> Verify page Loaded
    ...                Author              :       Niket Shinde
    [Arguments]  ${Username}    ${Password}
    Open CS360 Application
    Verify Login page Loaded
    Fill "Username" Field     ${Username}
    Fill "Password" Field     ${Password}
    Click "Login" Button
    WelcomeCS360.Verify Welcome page Loaded





