# ProjectName
GUI Test Automation Framework for Project

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [Python 3.x](https://www.python.org/downloads/)

* For test case development you can use any IDE which support python and [Robot Framework](https://robotframework.org/) (recommended [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)) 

* Dependencies

To install required libraries you can run below commands in windows command prompt

```
pip install robotframework
pip install robotframework-seleniumlibrary
pip install robotframework-requests
pip install requests
pip install robotframework-databaselibrary
pip install robotframework-pabot

pip install pandas
```

* [Tool_RobotFramework](https://tsutfs.tieto.com/EUCollection/TietoSmartUtility/Test%20Automation%20PF%20RT/_git/TestAutomation_PF_RTL?path=%2F&version=GBmaster&_a=contents)

### Installing

Follow below steps to clone project to local machine

1. Login to Git

```
git config --global user.name "YOUR_USERNAME"
git config --global user.email "YOUR_Email"
```

2. Change Authentication method

```
git config --global http.sslVerify false 
```

2. Clone project

```
git clone TFS project repo path
```

## Running the tests

You can execute test case or suite from command command prompt

* To run single test from robot test suite (.robot file)
```
robot -d "ResultFolderpath" -x "xUnit XML Folder path" --variable ENV:PF --variable BRW:chrome --test "Test Name" "path\Test Suite Name.robot"
```
* To run robot suite
```
robot -d "ResultFolderpath" -x "xUnit XML Folder path" --variable ENV:PF --variable BRW:chrome "path\TestSuiteName.robot"
```

## Useful links for Robot Framework

1. RF Offical Website https://robotframework.org/
2. RF User Guide  http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
3. RF Build-in keywords documentation : http://robotframework.org/robotframework/#standard-libraries


## Versioning

1.0

## Team
* **Niket Shinde** - *contributor* - [email](niket.shinde@tieto.com)

## Acknowledgments 



