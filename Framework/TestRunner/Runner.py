import robot
import datetime
import shutil
import os


# Test Case Suite Name:
testcase_suite_name = 'C:/Users/shindnik/AT_Framework/TestAutomation_PF_RTL/Tests/OrderPortal.robot'
# Test Case Name
testcase_name = 'OrderPortal-4105.10_Business Rule Check_Verify the business rule validation for Reason Code through Order Portal'
result_folder = ""

env = 'DEV'

path = os.path.abspath(os.getcwd() + "/../")+"\\"
now = datetime.datetime.today()
nTime = now.strftime("%Y-%m-%d_%H-%M-%S")
source = path+"results\\"
dest = os.path.join(source, testcase_name+nTime)
if not os.path.exists(dest):
    os.makedirs(dest)

if testcase_name == "":
    rc = robot.run_cli(
        ["-d", dest, "--timestampoutputs", path + 'Tests\\' + testcase_suite_name + ".robot"],
        exit=True)
else:
    rc = robot.run_cli(["-d", dest,  "--timestampoutputs", '--test', testcase_name, path+'Tests\\'+
                        testcase_suite_name + ".robot"], exit=True)




