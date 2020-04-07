import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from config.VarConfig import *
from basic.RunTestcase import RunTestcase

if __name__ == "__main__":
    # print(testcase_path)
    # print(testcase_list)
    for dataFilePath in testcase_list:
        runTestcase = RunTestcase(dataFilePath)
        runTestcase.runTestcase()