*** Settings ***
Documentation  All Test related to CS360 App
Metadata  Version  1.0
Metadata  Executed By  %{USERNAME}
#Metadata  Executed At    %{HOST}
#Metadata  Environment  ${ENV}
Force Tags      CS360 Smoke Test
Default Tags    Smoke Test

# Framework Library
Resource  ../../Framework/RobotLibraries/Commonkeywords.Robot

# Keywords Files
Resource  ../Apps/CS360/CS360Keywords.robot


# Configure Test Run
Suite Setup  Before Suite Start
Test Setup  Before Web Test Start
Test Teardown  After Web Test End
Suite Teardown  After Suite End
#Test Timeout  20s


*** Test Cases ***
# Run Commod : robot -d results tests/SanityTests/CS360SmokeTest.robot
Check login to CS360
    [Documentation]    New Sales Move In
    ...                Author              :       Niket Shinde
    [Tags]  CS360SmokeTest  RegressionSuite Critcal
    CS360Keywords.Login  ITR1





