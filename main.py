import sys
import os

# 将项目根目录加入python库搜索路径
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from config.VarConfig import *
from basic.RunTestcase import RunTestcase
from util.ReportTemplate import ReportTemplate

if __name__ == "__main__":
    for dataFilePath in testcase_list:
        runTestcase = RunTestcase(dataFilePath)
        runTestcase.runTestcase()
    reportTemplate = ReportTemplate()
    reportTemplate.reportTemplate(reportTemplate.statistics(excel_files=testcase_list),reportTemplate.getResult(excel_files=testcase_list))