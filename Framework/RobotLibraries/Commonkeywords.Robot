*** Settings ***
Documentation  All common Keywords

#.py Files
Library  ../PyLibraries/Generic.py
Library  ../PyLibraries/DataManger.py
Library  ../PyLibraries/APIManger.py
Library  SeleniumLibrary
Library  Collections
Library  String
Library  OperatingSystem
Library  copy


# .Robot Files
Resource  EnvironmentVariables.robot

*** Variables ***


*** Keywords ***
Before Suite Start
    [Documentation]  Before start of Test Suite run
    ...              Author              :       Niket Shinde

    ${str} =  Replace String  ${CURDIR}  \\RobotLibraries  ${EMPTY}
    set global variable  ${FRAMEWORK_PATH}  ${str}


    ${iniFilePath} =  Concatenate String  ${FRAMEWORK_PATH}   \\Config\\${GLOBAL_ENVIRONMENT_FILE_NAME}
    ${RUN_SETTINGS}=  ini to dictionary  ${iniFilePath}  Settings

    set global variable  ${PROJECT_NAME}  ${RUN_SETTINGS['PROJECT_NAME']}

    ${str} =  Replace String  ${FRAMEWORK_PATH}  ${FRAMEWORK_NAME}  ${EMPTY}
    set global variable  ${PROJECT_PATH}  ${str}${PROJECT_NAME}


    ${iniFilePath} =  Concatenate String  ${PROJECT_PATH}  \\Environment\\${PROJECT_ENVIRONMENT_FILE_NAME}
    ${RUN_SETTINGS}=  ini to dictionary  ${iniFilePath}  ProjectSettings  ${RUN_SETTINGS}
    set global variable  ${RUN_SETTINGS}

    Set All Global Variables

    
    ${ENVIRONMENT}=  ini to dictionary  ${iniFilePath}  ${ENV}
    set global variable   ${ENVIRONMENT}
    # Log  Environment Dictionary:${ENVIRONMENT}


    ${APIFilePath} =  Concatenate String  ${PROJECT_PATH}   \\Environment\\${WSDL_ENVIRONMENT_FILE_NAME}
    ${ENVIRONMENT_API}=  Get Web Service Environment Variables  ${ENV}  ${APIFilePath}
    set global variable  ${ENVIRONMENT_API}
    Log  API Environment Dictionary:${ENVIRONMENT_API}
    #Set To Dictionary  ${SUITE METADATA}  Executed By=%{USERNAME}
    #set global variable  ${SUITE METADATA}


After Suite End
    [Documentation]  After Suite End
    ...              Author              :       Niket Shinde
    No operation



Set All Global Variables
    [Documentation]  Set values for all Global Variables
    ...              Author              :       Niket Shinde
    ${ENV}=  set value  ${ENV}  ${RUN_SETTINGS['ENVIRONMENT']}
    ${ENV}=  Get Variable Value  ${ET}  ${ENV}
    set global variable  ${ENV}
    Set Suite Metadata  Environment  ${ENV}

    Set Suite Metadata  Executed By   %{USERNAME}

    ${BROWSER}=  set value  ${BROWSER}  ${RUN_SETTINGS['BROWSER']}
    ${BROWSER}=  Get Variable Value  ${BR}  ${BROWSER}
    set global variable  ${BROWSER}
    Set Suite Metadata  Browser  ${BROWSER}

    ${TIMEOUT_WAIT}=  set value  ${TIMEOUT_WAIT}  ${RUN_SETTINGS['WAIT']}
    set global variable  ${TIMEOUT_WAIT}

    ${IMPLICIT_WAIT}=  set value  ${IMPLICIT_WAIT}  ${RUN_SETTINGS['IMPLICIT_WAIT']}
    set global variable  ${IMPLICIT_WAIT}

    ${LOG_LEVEL}=  set value  ${LOG_LEVEL}  ${RUN_SETTINGS['LOG_LEVEL']}
    set global variable  ${LOG_LEVEL}

    ${CSV_DELIMITER}=  set value  ${CSV_DELIMITER}  ${RUN_SETTINGS['CSV_DILIMITER']}
    set global variable  ${CSV_DELIMITER}

    ${GLOBAL_DATA_FILE_NAME}=  set value  ${GLOBAL_DATA_FILE_NAME}  ${RUN_SETTINGS['DATA_FILE_NAME']}
    set global variable  ${GLOBAL_DATA_FILE_NAME}


    ${WSDL_ENVIRONMENT_FILE_NAME}=  set value  ${WSDL_ENVIRONMENT_FILE_NAME}  ${RUN_SETTINGS['WSDL_ENVIRONMENT_FILE_NAME']}
    set global variable  ${WSDL_ENVIRONMENT_FILE_NAME}


Before Web Test Start
    [Documentation]    Open browser
    ...                Author              :       Niket Shinde
    ${TC_FOLDER}=  Fetch From Left  ${TEST NAME}  -
    ${TC_FOLDER}=  Strip String  ${TC_FOLDER}
    ${TC_FOLDER}=  Set Variable If  "${TC_FOLDER}"=="${TEST NAME}"  ${None}  ${TC_FOLDER}
    set global variable  ${TC_FOLDER}

    ${TC_PATH}=  Set Variable If  "${TC_FOLDER}"=="${None}"  ${PROJECT_PATH}\\TestData\\${ENV}\\${TEST NAME}
                                                ...  ${PROJECT_PATH}\\TestData\\${ENV}\\${TC_FOLDER}\\${TEST NAME}
    set global variable  ${TC_PATH}
    Update Dictionary for Test Data
    ${BROWSER}=  set value  ${BROWSER}  ${GLOBAL_TEST_DICTONARY['ITR1']}    key=BROWSER
    ${bool}=  Is Chrome  ${BROWSER}
    Run keyword if  "${bool}" == "True"   Run Test In Chrome Browser
    ...  ELSE  open browser  about:blank  ${BROWSER}
    Maximize Browser Window
    Delete All Cookies
    Set Selenium Implicit Wait  ${IMPLICIT_WAIT}
    &{API_DICTIONARY}=  Create Dictionary  auth_token=${EMPTY}
    set global variable  ${API_DICTIONARY}



After Web Test End
    [Documentation]    Close all browser
    ...                Author              :       Niket Shinde
     no operation

#    Execute Javascript  ${GLOBAL_FRAMEWORK_PATH}//javascript//LoadjQuery.js
#    sleep  2s
#    Execute Javascript  $.growl({title:'GET',message:'Hi'});
#    Execute Javascript  $.growl.warning({ title: 'Warning!', message: 'your warning message goes here' });
#    Execute Javascript  $.growl.notice({ title: 'Notice', message: 'your notice message goes here' });
#    Execute Javascript  $.growl.error({ title: 'ERROR', message: 'Some exception is coming' });
    #close browser
    # close all browsers


Run Test In Chrome Browser
    [Documentation]   Open chrome with image disable or enable mode
    ...                Author              :       Niket Shinde
    ${flag}=  Set Variable If  "${RUN_SETTINGS['DISABLE_IMAGES']}"=="TRUE"  ${2}  ${1}
    ${options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
    ${desired caps}=     Create Dictionary  profile.managed_default_content_settings.images=${flag}
    Call Method    ${options}    add_experimental_option  prefs  ${desired caps}
    create webdriver   ${BROWSER}   chrome_options=${options}

Update Dictionary for Test Data
    [Documentation]    Get Data To Dictionary from Test data and Global data
    ...                Author              :       Niket Shinde

    # Get data from Global CSV
    ${CSVFilePath} =  Concatenate String  ${PROJECT_PATH}  \\TestData\\
    ${DATA_DICTIONARY}=  Get Global Test Data To Dictionary  ${CSVFilePath}  ${ENV}  ${CSV_DELIMITER}  ${GLOBAL_DATA_FILE_NAME}
    set global variable  ${DATA_DICTIONARY}

    # Get data from Test case data CSV
    ${GLOBAL_TEST_DICTONARY} =  get test data to dictionary  ${TC_PATH}  ${CSV_DELIMITER}
    set global variable  ${GLOBAL_TEST_DICTONARY}
    ${ORIGINAL_TEST_DICTONARY}=  copy.deepcopy  ${GLOBAL_TEST_DICTONARY}
    #${ORIGINAL_TEST_DICTONARY}=  get test data to dictionary  ${CSVTestFilePath}  ${GLOBAL_CSV_DELIMITER}
    set global variable  ${ORIGINAL_TEST_DICTONARY}


Keyword Setup
    [Documentation]    This is setup keyword for test step
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}
    ${DATA_DICTIONARY} =  marge dictionaries  ${DATA_DICTIONARY}  ${ORIGINAL_TEST_DICTONARY['${ITR}']}
    ${DATA_DICTIONARY} =  update dictionary  ${DATA_DICTIONARY}  ${GLOBAL_TEST_DICTONARY}  ${PROJECT_PATH}\\TestData\\  ${CSV_DELIMITER}  ${ITR}
    set global variable  ${DATA_DICTIONARY}


Keyword Teardown
    [Documentation]    This is teardown keyword for test step
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}
    log  ${API_DICTIONARY}  level=DEBUG
    ${GLOBAL_TEST_DICTONARY} =  marge Test dictionaries  ${ITR}  ${GLOBAL_TEST_DICTONARY}  ${DATA_DICTIONARY}
    set global variable  ${GLOBAL_TEST_DICTONARY}
    log  ${GLOBAL_TEST_DICTONARY}  level=DEBUG
    test_dictionary_to_csv  ${GLOBAL_TEST_DICTONARY}  ${OUTPUT DIR}\\${TEST NAME}_TestData_${ENV}  ${CSV_DELIMITER}
    log  Test data '${OUTPUT DIR}\\${TEST NAME}_TestData_${ENV}.csv' file create in result folder
    # ${filename} =  Concatenate String  //testdata/  ${TEST NAME}  _TestData.csv
    # ${filename} =  Concatenate String  <a href="file:  ${filename}  ">test data file</a>
    # log  ${filename}  html=True


Send API Request
    [Documentation]     To send API request
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}  ${service_name}  ${function_name}
    ${dictionay}=  send request  ${ENVIRONMENT_API}  ${PROJECT_PATH}  ${API_DICTIONARY}  ${service_name}  ${function_name}
    Should Be Equal As Integers  ${dictionay['status']}  ${200}   msg=Response Status code should be 200 i.e. OK
    [Return]  ${dictionay['response']}


Get Access token
    [Documentation]  to get access token using access token API
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}  ${TokenType}
    ${response}=  Send API Request  ${ITR}  Token  ${TokenType}
    ${token}=  get value from json  ${response}  access_token
    Set To Dictionary  ${API_DICTIONARY}  TOKEN=Bearer${SPACE}${token}
    set global variable  ${API_DICTIONARY}


Add value to Template
    [Documentation]  replace values from API templates
    ...                Author              :       Niket Shinde
    [Arguments]  ${key}  ${Value}
    log  '$${key}$' key replaced by '${Value}' value in template.
    Set To Dictionary  ${API_DICTIONARY}  ${key}=${Value}
    set to dictionary  ${DATA_DICTIONARY}  ${key}=${Value}
    set global variable  ${API_DICTIONARY}
    set global variable  ${DATA_DICTIONARY}


# example : Commonkeywords.Generate Fake TestData In CSV  sv_SE  10  fake_cust_data
Generate Fake TestData In CSV
    [Documentation]  to generate fake data
    ...                Author              :       Niket Shinde
    [Arguments]  ${region}  ${Number_of_Customer}  ${file_path}
    ${fake_data}=  generate test data  ${region}  ${Number_of_Customer}  ${GLOBAL_FRAMEWORK_PATH}Results\\${file_path}


Create EDI File on Server Location
    [Documentation]  Create EDi File
    ...                Author              :       Niket Shinde
    [Arguments]  ${ITR}  ${message_type}
    ${edi_file_path}=  set variable  ${PROJECT_PATH}/RequestTemplates/ProdatMessages/${message_type}.edi
    ${EDI_file_location}=  Create Edi File  ${edi_file_path}  ${API_DICTIONARY}  ${PROJECT_PATH}/  ${ENVIRONMENT['EDI_PATH']}

EDI File - Process UTIL Message
    [Documentation]    Create EDI File and Copy to Server location
    ...                Author             :       Snehal Rakshe
    [Arguments]  ${ITR}  ${message_type}
    Commonkeywords.Keyword Setup  ${ITR}
    ${CREATION_DATE}=  Get Timestamp  ${DATA_DICTIONARY['EDI_CREATION_DATE']}  ${4}
    Commonkeywords.Add value to Template  CREATION_DATE  ${CREATION_DATE}
    Commonkeywords.Add value to Template  DELIVERYSITE_ID  ${DATA_DICTIONARY['DS_ID']}
    Commonkeywords.Add value to Template  ERRAND_REF  ${DATA_DICTIONARY['ERRAND_REF']}
    Commonkeywords.Add value to Template  MESSAGE_ID  ${DATA_DICTIONARY['MESSAGE_ID']}
    Commonkeywords.Add value to Template  METER_NO  ${DATA_DICTIONARY['ERRAND_REF']}
    ${METER_READING_START_DATE}=  Get Timestamp  ${DATA_DICTIONARY['EDI_METER_READING_START']}  ${2}
    Commonkeywords.Add value to Template  EDI_METER_READING_START  ${METER_READING_START_DATE}
    ${METER_READING_END_DATE}=  Get Timestamp  ${DATA_DICTIONARY['EDI_METER_READING_END']}  ${2}
    Commonkeywords.Add value to Template  EDI_METER_READING_END  ${METER_READING_END_DATE}


    Commonkeywords.Create EDI File on Server Location  ${ITR}  ${message_type}
    [Teardown]  Commonkeywords.Keyword Teardown  ${ITR}


Sleep App
    sleep  ${RUN_SETTINGS['SLEEP_TIME']}



