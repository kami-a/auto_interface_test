import sys
import os

# 获取项目根目录
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

report_path = rootPath + "\\report"
log_path = rootPath + "\\log"
testcase_path = rootPath + "\\testcase"

# 获取测试用例Excel文档，放入testcase_list列表
global testcase_list
testcase_list = []
for parent,dirnames,filenames in os.walk(testcase_path):
    for filename in filenames:
        if filename.endswith('xlsx'):
            file = os.path.join(parent,filename)
            testcase_list.append(file)


# 测试用例表
testCase_testCaseName = 2
testCase_frameWorkName = 4
testCase_apiSheetName = 5
testCase_dataSourseSheetName = 6
testCase_isExecute = 7
testCase_runTime = 8
testCase_testResult = 9
testCase_executeNum = 10
testCase_successNum = 11

# 接口用例表
api_name = 2
api_isExecute = 3
api_url = 4
api_requestMethod = 5
api_requestHeader = 6
api_requestData = 7
api_checkData = 8
api_responseData = 9
api_runTime = 10
api_testResult = 11

# 数据源表
dataSource_name = 2
dataSource_isExcute = 8
dataSource_runtime = 9
dataSource_result = 10
