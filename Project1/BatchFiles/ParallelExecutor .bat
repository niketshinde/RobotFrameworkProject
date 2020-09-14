@echo on
REM Robot test run started
:: Pabot -d "Result Folder path" --variable ET:INT --variable BR:gc test suite folder path
Pabot -d C:\Users\shindnik\PFAutomationGitRepo\TestAutomation_PF_RTL\Results --variable ET:PF --variable BR:IE C:\Users\shindnik\PFAutomationGitRepo\TestAutomation_PF_RTL\Tests
PAUSE