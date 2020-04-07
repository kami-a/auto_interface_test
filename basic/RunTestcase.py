# 运行测试用例类
# 本文件用于对执行测试用例业务场景的封装

from basic.Testcase import Testcase
from util.OperateExcel import OperateExcel
from config.VarConfig import *
from util.Log import *
from basic.IntegrateRequest import IntegrateRequest
import traceback

#创建Log对象
log = Logger(log_path +'\\testLog.log',level='info')

class RunTestcase(object):
    def __init__(self, excelPathAndName = excelPathAndName):
        self.testcases = Testcase(excelPathAndName = excelPathAndName)
        self.ir = IntegrateRequest()

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
                    # 获取当前执行用例所使用的框架类型
                    useFrameWorkName = self.testcases.operateExcel.getCellOfValue(caseSheet, rowNo=idx + 2, colsNo=testCase_frameWorkName)
                    # 获取测试用例列中，当前行执行的接口用例的sheet名
                    apiSheetName = self.testcases.operateExcel.getCellOfValue(caseSheet, rowNo=idx + 2, colsNo=testCase_apiSheetName)
                    log.logger.info('%s'%(apiSheetName))
                    if useFrameWorkName == '数据':
                        log.logger.info('***********调用数据驱动************')
                        # 获取测试用例表中，当前执行，执行框架为数据驱动的用例所使用的数据sheet名
                        dataSheetName = self.testcases.operateExcel.getCellOfValue(caseSheet, rowNo=idx + 2, colsNo=testCase_dataSourseSheetName)
                        # 获取当前执行行接口测试用例的sheet对象
                        apiSheetObj = self.testcases.operateExcel.getSheetByName(apiSheetName)
                        # 获取当前执行行接口测试用例使用的数据sheet对象
                        dataSheetObj = self.testcases.operateExcel.getSheetByName(dataSheetName)
                        # 通过数据驱动框架执行添加数据
                        result = dataDrivenFun(apiSheetObj, dataSheetObj)
                        if result:
                            log.logger.info('用例"%s"执行成功' % (caseName))
                            successfulCase += 1
                            self.testcases.writeTestResult(caseSheet, rowNo=idx + 2, colsNo="testCase", testResult="pass")
                        else:
                            log.logger.error('用例"%s"执行失败' % (caseName))
                            self.testcases.writeTestResult(caseSheet, rowNo=idx + 2, colsNo="testCase", testResult="failed")
                    elif useFrameWorkName == "关键字":
                        log.logger.info('*************调用关键字驱动****************')
                        apiSheetObj = self.testcases.getSheetByName(apiSheetName)
                        apiNums = self.testcases.operateExcel.getRowsNumber(apiSheetObj)
                        log.logger.info('测试用例共%s步' % (apiNums-1))
                        # 通过关键字驱动框架执行接口
                        result = keywordDrivenFun(apiSheetObj)
                        self.testcases.writeTestResult(caseSheet, rowNo=idx + 2, colsNo="testCase", testResult=result)
        except Exception as e:
            log.logger.error('出现异常' + traceback.format_exc())

    def keywordDrivenFun(self,apiSheetObj):
        apiNums = self.testcases.operateExcel.getRowsNumber(apiSheetObj)
        # 成功接口数
        successfulApi = 0
        # 执行接口数
        executeApi = 0
        for index in range(2, apiNums + 1):
            # 因为第一行标题行无须执行
            # 获取接口用例sheet中第index行对象
            apiRow = self.testcases.operateExcel.getRow(apiSheetObj, index)
            # 获取接口名
            apiName = apiRow[api_name - 1].value
            # 获取接口的url
            url = apiRow[api_url - 1].value
            # 获取接口的请求方法
            method = apiRow[api_requestMethod - 1].value
            # 获取接口请求头
            header = apiRow[api_requestHeader - 1].value
            # 获取接口请求体
            requestData = apiRow[api_requestData - 1].value
            # 获取是否执行
            isExecute = apiRow[api_isExecute].value
            # 获取检测数据
            checkData = apiRow[api_checkData].value
            # 判断接口是否执行
            if isExecute == 'y':
                executeApi += 1
                res = self.ir.main_req(method, url, requestData, header)
                # 判断接口是否执行成功
                if (checkData in res):
                    successfulApi += 1
                    log.logger.info('接口：%s执行成功' % (apiName))
                    # 接口执行成功写如接口用例Excel
                    self.testcases.writeTestResult(apiSheetObj, rowNo=index, colsNo="api", testResult="pass")
                    return (executeApi,successfulApi)
                else:
                    log.logger.info('接口：%s执行失败' % (apiName))
                    # 接口执行失败写如接口用例Excel
                    self.testcases.writeTestResult(apiSheetObj, rowNo=index, colsNo="api", testResult="failed")
                    return (executeApi,successfulApi)
            else:
                # 接口未执行写入接口用例Excel
                self.testcases.writeTestResult(apiSheetObj, rowNo=index, colsNo="api", testResult="none")
                return (executeApi,successfulApi)
                        

    def dataDrivenFun(self,apiSheetObj, dataSheetObj):
        try:
            # 获取数据源表中是否执行列对象
            dataIsExecuteColumn = self.testcases.operateExcel.getColumn(dataSheetObj,dataSource_isExcute)
            # 获取数据源表中“接口数据名”列对象
            nameColumn = self.testcases.operateExcel.getColumn(dataSheetObj,dataSource_name)
            # 获取接口用例表中存在数据区域的行数
            apiNums = self.testcases.operateExcel.getRowsNumber(apiSheetObj)
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
                    # 定义记录执行成功api数
                    successfulApi = 0
                    # 定义执行的api数
                    executeApi = 0
                    for index in range(2,apiNums+1):
                        # 因为第一行标题行无须执行
                        # 获取接口用例sheet中第index行对象
                        apiRow = self.testcases.operateExcel.getRow(apiSheetObj, index)
                        # 获取接口名
                        apiName = apiRow[api_name - 1].value
                        # 获取接口的url
                        url = apiRow[api_url - 1].value
                        # 获取接口的请求方法
                        method = apiRow[api_requestMethod - 1].value
                        # 获取接口请求头
                        header = apiRow[api_requestHeader - 1].value
                        # 获取接口请求体
                        requestData = apiRow[api_requestData - 1].value
                        # 获取是否执行
                        isExecute = apiRow[api_isExecute].value
                        # 获取检测数据
                        checkData = apiRow[api_checkData].value
                        if header and header.isalpha() and len(header)==1:
                            # 如果header变量是字母且为1，说明有操作值从数据源表中
                            # 根据坐标获取对应单元格的数据
                            colsNo=ord(header.upper())-64
                            header = self.testcases.operateExcel.getCellOfValue(dataSheetObj,rowNo=idx + 2, colsNo=colsNo)
                        if requestData and requestData.isalpha() and len(requestData)==1:
                            # 如果requestData变量是字母且为1，说明有操作值从数据源表中
                            # 根据坐标获取对应单元格的数据
                            colsNo=ord(requestData.upper())-64
                            requestData = self.testcases.operateExcel.getCellOfValue(dataSheetObj,rowNo=idx + 2, colsNo=colsNo)
                        if checkData and checkData.isalpha() and len(checkData) == 1:
                            # 如果checkData变量是字母且为1，说明有操作值从数据源表中
                            # 根据坐标获取对应单元格的数据中的页面动作函数调用的字符串表示
                            colsNo=ord(checkData.upper())-64
                            checkData = self.testcases.operateExcel.getCellOfValue(dataSheetObj,rowNo=idx + 2, colsNo=colsNo)
                        # 判断接口是否执行

                        
                        if isExecute == 'y':
                            executeApi += 1
                            res = self.ir.main_req(method, url, requestData, header)
                            # 判断接口是否执行成功
                            if (checkData in res):
                                successfulApi += 1
                                log.logger.info('接口：%s执行成功' % (apiName))
                                # 接口执行成功写如接口用例Excel
                                self.testcases.writeTestResult(apiSheetObj, rowNo=index, colsNo="api", testResult="pass")
                                return (executeApi,successfulApi)
                            else:
                                log.logger.info('接口：%s执行失败' % (apiName))
                                # 接口执行失败写如接口用例Excel
                                self.testcases.writeTestResult(apiSheetObj, rowNo=index, colsNo="api", testResult="failed")
                                return (executeApi,successfulApi)
                        else:
                            # 接口未执行写入接口用例Excel
                            self.testcases.writeTestResult(apiSheetObj, rowNo=index, colsNo="api", testResult="none")
                            return (executeApi,successfulApi)

        except Exception as e:
            raise e