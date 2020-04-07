# 运行测试用例类
# 本文件用于对执行测试用例业务场景的封装

from basic.Testcase import Testcase
from util.OperateExcel import OperateExcel
from config.VarConfig import *
from util.Log import *
from basic.IntegrateRequest import IntegrateRequest
import traceback

#创建Log对象
log = Logger(log_path +'/testLog.log',level='info')

class RunTestcase(object):
    def __init__(self, excelPathAndName):
        self.testcases = Testcase(excelPathAndName = excelPathAndName)
        self.ir = IntegrateRequest()
    
    # 数据源驱动方法
    def dataDrivenFun(self,apiRow, dataSheet):
        try:
            # 获取数据源表中是否执行列对象
            dataIsExecuteColumn = self.testcases.operateExcel.getColumn(dataSheet,dataSource_isExcute)
            # 获取数据源表中“接口数据名”列对象
            nameColumn = self.testcases.operateExcel.getColumn(dataSheet,dataSource_name)
            # 记录成功执行的数据条数
            successDatas = 0
            # 记录被设置为执行的数据条数
            executeDatas = 0
            for idx,data in enumerate(dataIsExecuteColumn[1:]):
                # 遍历数据源表，准备进行数据驱动测试
                # 因为第一行是标题行，所以从第二行开始遍历
                if data.value == 'y':
                    log.logger.info('开始执行用例"%s"'%(nameColumn[idx+1].value))
                    executeDatas +=1
                    # 获取接口的url
                    url = apiRow[api_url - 1].value
                    # 获取接口的请求方法
                    method = apiRow[api_requestMethod - 1].value
                    # 获取接口请求头
                    header = apiRow[api_requestHeader - 1].value
                    # 获取接口请求体
                    requestData = apiRow[api_requestData - 1].value
                    # 获取是否执行
                    isExecute = apiRow[api_isExecute - 1].value
                    # 获取检测数据
                    checkData = apiRow[api_checkData - 1].value
                    if header and header.isalpha() and len(header)==1:
                        # 如果header变量是字母且为1，说明有操作值从数据源表中
                        # 根据坐标获取对应单元格的数据
                        colsNo=ord(header.upper())-64
                        header = self.testcases.operateExcel.getCellOfValue(dataSheet,rowNo=idx + 2, colsNo=colsNo)
                    if method and method.isalpha() and len(method)==1:
                        # 如果method变量是字母且为1，说明有操作值从数据源表中
                        # 根据坐标获取对应单元格的数据
                        colsNo=ord(method.upper())-64
                        method = self.testcases.operateExcel.getCellOfValue(dataSheet,rowNo=idx + 2, colsNo=colsNo)
                    if requestData and requestData.isalpha() and len(requestData)==1:
                        # 如果requestData变量是字母且为1，说明有操作值从数据源表中
                        # 根据坐标获取对应单元格的数据
                        colsNo=ord(requestData.upper())-64
                        requestData = self.testcases.operateExcel.getCellOfValue(dataSheet,rowNo=idx + 2, colsNo=colsNo)
                    if checkData and checkData.isalpha() and len(checkData) == 1:
                        # 如果checkData变量是字母且为1，说明有操作值从数据源表中
                        # 根据坐标获取对应单元格的数据中的页面动作函数调用的字符串表示
                        colsNo=ord(checkData.upper())-64
                        checkData = self.testcases.operateExcel.getCellOfValue(dataSheet,rowNo=idx + 2, colsNo=colsNo)
                    res = self.ir.main_req(method, url, requestData, header)
                    if (checkData == '' or checkData == 'none' or checkData == None):
                        if (res.status_code == 200 or res.status_code == 302):
                            successDatas += 1
                            log.logger.info('数据：%s执行成功' % (nameColumn[idx+1].value))
                            # 接口执行成功写入接口用例Excel
                            self.testcases.writeTestResult(dataSheet, rowNo=idx + 2, colsNo="dataSheet", testResult=("pass",res.text))
                        else:
                            log.logger.info('数据：%s执行失败' % (nameColumn[idx+1].value))
                            # 接口执行失败写入接口用例Excel
                            self.testcases.writeTestResult(dataSheet, rowNo=idx + 2, colsNo="dataSheet", testResult=("failed",res.text))
                    else:
                        if (checkData in res.text):
                            successDatas += 1
                            log.logger.info('数据：%s执行成功' % (nameColumn[idx+1].value))
                            # 接口执行成功写入接口用例Excel
                            self.testcases.writeTestResult(dataSheet, rowNo=idx + 2, colsNo="dataSheet", testResult=("pass",res.text))
                        else:
                            log.logger.info('数据：%s执行失败' % (nameColumn[idx+1].value))
                            # 接口执行失败写入接口用例Excel
                            self.testcases.writeTestResult(dataSheet, rowNo=idx + 2, colsNo="dataSheet", testResult=("failed",res.text))
                else:
                    # 数据源未执行写入接口用例Excel
                        self.testcases.writeTestResult(dataSheet, rowNo=idx + 2, colsNo="dataSheet", testResult=("none","none"))
            if successDatas == executeDatas:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def runTestcase(self):
        try:
            # 获取测试用例表
            caseSheet = self.testcases.getCasesheet()
            # 成功用例数
            successfulCase = 0
            # 执行用例数
            executeCase = 0
            # 获取是否执行列对象
            isExecuteColumn = self.testcases.getExecuteColumn()
            for idx,i in enumerate(isExecuteColumn[1:]):
                # 获取当前执行的用例名
                caseName = self.testcases.operateExcel.getCellOfValue(caseSheet, rowNo=idx + 2,colsNo=testCase_testCaseName)
                if i.value.lower() == 'y':
                    executeCase += 1
                    # 获取测试用例列中，当前行执行的接口用例的sheet名
                    apiSheetName = self.testcases.operateExcel.getCellOfValue(caseSheet, rowNo=idx + 2, colsNo=testCase_apiSheetName)
                    log.logger.info('%s'%(apiSheetName))
                    # 获取当前执行行接口测试用例的sheet对象
                    apiSheet = self.testcases.operateExcel.getSheetByName(apiSheetName)
                    # 获取接口用例中的接口数
                    apiNums = self.testcases.operateExcel.getRowsNumber(apiSheet)
                    # 成功接口数
                    successfulApi = 0
                    # 执行接口数
                    executeApi = 0
                    for index in range(2,apiNums+1):
                        # 获取当前执行用例所使用的框架类型
                        useFrameWorkName = self.testcases.operateExcel.getCellOfValue(apiSheet, rowNo=index, colsNo=api_frameWorkName)
                        # 获取接口用例sheet中第index行对象
                        apiRow = self.testcases.operateExcel.getRow(apiSheet, index)
                        # 获取接口名
                        apiName = apiRow[api_name - 1].value
                        # 获取是否执行
                        isExecute = apiRow[api_isExecute - 1].value
                        if isExecute == 'y':
                            executeApi += 1
                            if useFrameWorkName == '数据':
                                log.logger.info('***********调用数据驱动************')
                                # 获取测试用例表中，当前执行，执行框架为数据驱动的用例所使用的数据sheet名
                                dataSheetName = apiRow[api_dataSourseSheetName - 1].value
                                # 获取当前执行行接口测试用例使用的数据sheet对象
                                dataSheet = self.testcases.operateExcel.getSheetByName(dataSheetName)
                                # 通过数据驱动框架执行添加数据
                                result = self.dataDrivenFun(apiRow, dataSheet)
                                if result:
                                    successfulApi += 1
                                    log.logger.info('接口：%s执行成功' % (apiName))
                                    # 接口执行成功写入接口用例Excel
                                    self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("pass",""))
                                else:
                                    log.logger.info('接口：%s执行失败' % (apiName))
                                    # 接口执行失败写入接口用例Excel
                                    self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("failed",""))
                            elif useFrameWorkName == "关键字":
                                # log.logger.info('*************调用关键字驱动****************')
                                # 获取接口的url
                                url = apiRow[api_url - 1].value
                                # 获取接口的请求方法
                                method = apiRow[api_requestMethod - 1].value
                                # 获取接口请求头
                                header = apiRow[api_requestHeader - 1].value
                                if (header == '' or header == 'none'):
                                    header = None
                                # 获取接口请求体
                                requestData = apiRow[api_requestData - 1].value
                                if (requestData == '' or requestData == 'none'):
                                    requestData = None
                                # 获取检测数据
                                checkData = apiRow[api_checkData - 1].value
                                res = self.ir.main_req(method, url, requestData, header)
                                # 判断接口是否执行成功
                                result = checkData in res
                                if (checkData == '' or checkData == 'none' or checkData == None):
                                    if (res.status_code == 200 or res.status_code == 302):
                                        successfulApi += 1
                                        log.logger.info('接口：%s执行成功' % (apiName))
                                        # 接口执行成功写入接口用例Excel
                                        self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("pass",res.text))
                                    else:
                                        log.logger.info('接口：%s执行失败' % (apiName))
                                        # 接口执行失败写入接口用例Excel
                                        self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("failed",res.text))
                                else:
                                    if (str(checkData) in res.text):
                                        successfulApi += 1
                                        log.logger.info('接口：%s执行成功' % (apiName))
                                        # 接口执行成功写入接口用例Excel
                                        self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("pass",res.text))
                                    else:
                                        log.logger.info('接口：%s执行失败' % (apiName))
                                        # 接口执行失败写入接口用例Excel
                                        self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("failed",res.text))
                        else:
                            log.logger.info('接口：%s未执行' % (apiName))
                            # 接口未执行写入接口用例Excel
                            self.testcases.writeTestResult(apiSheet, rowNo=index, colsNo="api", testResult=("none","none"))
                    self.testcases.writeTestResult(caseSheet,rowNo=idx + 2,colsNo="testCase",testResult=(executeApi,successfulApi))
                else:
                    # 在caseSheet表内写入该接口用例表执行0成功0
                    self.testcases.writeTestResult(caseSheet,rowNo=idx + 2,colsNo="testCase",testResult=(0,0))
        except Exception as e:
            log.logger.error('出现异常' + traceback.format_exc())

    

if __name__ == '__main__':
    runtestcase = RunTestcase(testcase_path + '/Testcases.xlsx')