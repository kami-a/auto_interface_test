import sys
import os
from config.VarConfig import *
from basic import RunTestcase

if __name__ == "__main__":
    # print(testcase_path)
    # print(testcase_list)
    for dataFilePath in testcase_list:
        runTestcase = RunTestcase(dataFilePath)
        runTestcase.runTestcase()