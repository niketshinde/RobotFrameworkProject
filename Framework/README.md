# Tool_RobotFramework

GUI Test Automation Framework 

## About Robot Framework
Robot Framework is a generic open source automation framework for acceptance testing, acceptance test driven development (ATDD). It has easy-to-use tabular test data syntax and it utilizes the keyword-driven testing approach. Its testing capabilities can be extended by test libraries implemented with Python, and users can create new higher-level keywords from existing ones using the same syntax that is used for creating test cases. [more](https://robotframework.org/)

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
git clone https://tsutfs.tieto.com/EUCollection/TietoSmartUtility/_git/Tool_RobotFramework
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

* **Marco Schaafsma** - *Manager* - [email](Marco.Schaafsma@tieto.com)

* **Niket Shinde** - *contributor* - [email](niket.shinde@tieto.com)
* **Sohan Ghanti** - *contributor* - [email](Sohan.Ghanti@tieto.com)
* **Anju Singh** - *contributor* - [email](Anju.Singh@tieto.com)


## Acknowledgments 



