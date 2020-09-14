*** Settings ***
Documentation  All Enviroment variables


*** Variables ***

# Framework Settings
${GLOBAL_ENVIRONMENT_FILE_NAME}  Settting.ini
${FRAMEWORK_NAME}  Tool_RobotFramework


# Project Settings
${PROJECT_ENVIRONMENT_FILE_NAME}  environment.ini


# Default Settings
${ENV}  PF
${BROWSER}  headlesschrome
${TIMEOUT_WAIT}  20s
${IMPLICIT_WAIT}  20 seconds
${LOG_LEVEL}  DEBUG     # loglevel are DEBUG TRACE INFO WARN ERROR NONE
${CSV_DELIMITER}  |
${GLOBAL_DATA_FILE_NAME}  GlobalData.csv
${WSDL_ENVIRONMENT_FILE_NAME}  WSDL_Environment.xml


# Suite Variables
&{DATA_DICTIONARY}
&{API_DICTIONARY}
&{GLOBAL_TEST_DICTONARY}
&{ORIGINAL_TEST_DICTONARY}
&{ENVIRONMENT}
&{ENVIRONMENT_API}
&{RUN_SETTINGS}
${ITR}
${FRAMEWORK_PATH}
${PROJECT_NAME}
${PROJECT_PATH}
${GLOBAL_RESULT_FOLDER}
${TC_FOLDER}
${TC_PATH}




