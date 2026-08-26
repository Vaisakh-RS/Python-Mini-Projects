from LogParser import LogParser
from ApiTest import fetchApi

class Combine:
    def __init__(self):
        self.parser=LogParser("D:/Py Projects/LogParser/sample.log")
        self.apiCall=fetchApi()

    def corelate(self):
        self.parser.parse()
        errorLogs=self.parser.filter_by_severity("ERROR")
        finalResult=[]
        for entry in errorLogs:
            ApiResult=self.apiCall.api_fetch("random")
            finalResult.append(ApiResult["activity"] + " "+ ApiResult["key"] + " "+entry.message)
        return finalResult

test=Combine()
print(test.corelate())
