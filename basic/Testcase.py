# 测试用例类
# 本文件用于对测试用例表操作的封装

from basic.ApiTestcase import ApiTestcase
from util.OperateExcel import OperateExcel
from config.VarConfig import *
import traceback

class Testcase(object):
    def __init__(self, excelPathAndName = excelPathAndName):
        self.apiTestcase = []
        self.operateExcel = OperateExcel(excelPathAndName = excelPathAndName)
        self.caseSheet = self.operateExcel.getSheetByName('测试用例')
        self.excelPathAndName = excelPathAndName

    def getCasesheet(self):
        return self.caseSheet
    
    def getExecuteColumn(self):
        return self.operateExcel.getColumn(caseSheet,testCase_isExecute)

    #用例或用例步骤执行结束后，像excel中执行结果信息
    def writeTestResult(self,sheetObj,rowNo,colsNo,testResult):
        #测试通过结果为绿色，失败为红色
        colorDict={"pass":"green","failed":"red","none":"green"}
        # 因为“测试用例”工作表和“用例步骤Sheet表”中都有测试执行时间和测试
        # 测试结果列，定义此字典对象是为了区分具体应该写哪个工作表
        colsDict = {
            "testCase":[testCase_runTime,testCase_testResult],
            "api":[api_runTime,api_testResult],
            "dataSheet":[dataSource_runtime,dataSource_result]}
        try:
            if colsNo == 'testCase':
                # 在测试用例sheet中，写入测试时间
                self.operateExcel.writeCellCurrentTime(sheetObj,rowNo=rowNo,colsNo=colsDict[colsNo][0])
                # 在测试用例sheet中，写入执行接口数
                self.operateExcel.writeCell(sheetObj, content=testResult[0],
                                rowNo=rowNo, colsNo=colsDict[colsNo][1], style=colorDict[testResult])
                # 在测试用例sheet中，写入成功接口数
                self.operateExcel.writeCell(sheetObj, content=testResult[1],
                                rowNo=rowNo, colsNo=colsDict[colsNo][1], style=colorDict[testResult])
            else:
                # 在接口用例或数据源sheet中，写入测试时间
                self.operateExcel.writeCellCurrentTime(sheetObj,rowNo=rowNo,colsNo=colsDict[colsNo][0])
                # 在接口用例或数据源sheet中，写入测试结果
                self.operateExcel.writeCell(sheetObj, content=testResult,
                                rowNo=rowNo, colsNo=colsDict[colsNo][1], style=colorDict[testResult])
        except Exception as e:
            print(u"写excel时发生异常,",+traceback.print_exc())