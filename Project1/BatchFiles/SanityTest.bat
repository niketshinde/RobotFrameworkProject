@echo on
REM Robot test run started
:: For single test 				robot -d "Result Folder path" --variable ET:INT --variable BR:gc --test "testCase Name" TestCasePath
:: For test	suite				robot -d "Result Folder path" --variable ET:INT --variable BR:gc --test "testCase Name" TestCasePath
robot -d C:\Users\shindnik\PFAutomationGitRepo\TestAutomation_PF_RTL\Results --variable ET:INT --variable BR:IE --test "Create Marketing List using API" C:\Users\shindnik\PFAutomationGitRepo\TestAutomation_PF_RTL\Tests\CRMSmokeTest.robot
