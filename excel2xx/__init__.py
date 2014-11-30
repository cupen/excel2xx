# encoding:UTF-8

__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'

import os
import re
import json
from collections import OrderedDict
from docopt import docopt
from xlrd import open_workbook

class Excel:

    XX_TYPE_LIST = 1
    XX_TYPE_DICT = 2

    def __init__(self, filePath, fieldRowNum = 2):
        self.__filePath = filePath
        self.__fieldRowNum = fieldRowNum
        self.__callback = None
        pass

    def __iter__(self):
        excelPath = self.__filePath
        beginRowNum = self.__fieldRowNum + 1
        endRowNum = 0
        fieldNameArr = next(foreach_excelRows(excelPath, 2, 2))

        wb = open_workbook(excelPath)
        sheet = wb.sheets()[0]
        pattern = re.compile("^\s*$")
        for row in range(wb.sheets()[0].nrows):
            if(row.numerator < beginRowNum - 1):
                continue

            if(endRowNum != 0 and row.numerator > endRowNum):
                break

            rowDict = OrderedDict()
            flag = False # 数据是否有效
            for colNum in range(sheet.ncols):
                cell = sheet.cell(row,colNum)
                if(colNum > len(fieldNameArr) -1 ):
                    continue

                if isinstance(cell.value, float) and cell.value == int(cell.value):
                    cell.value = int(cell.value)

                fieldName = fieldNameArr[colNum]
                if(fieldName and fieldName is not '' ):
                    rowDict[fieldName] = cell.value
                    if(not pattern.match(str(cell.value) if not isinstance(cell.value, str) else cell.value)):
                        flag = True
                    else:
                        pass

            if(flag):
                # print(keyValueMap)
                yield rowDict
        pass

    def __toList(self):
        jsonObj = []
        for _dict in self:
            jsonObj.append(_dict)
        return jsonObj

    def __toDict(self):
        jsonObj = OrderedDict()
        firstField = None
        for _dict in self:
            if not firstField:
                for tmp in _dict.keys():
                    firstField = tmp
                    break
            jsonObj[_dict[firstField]] = _dict
        return jsonObj

    def toOriginData(self, xxType = XX_TYPE_LIST):
        data = None
        if xxType == Excel.XX_TYPE_DICT:
            data = self.__toDict()
        elif xxType == Excel.XX_TYPE_LIST:
            data = self.__toList()
        else:
            data = None
        if self.__callback:
            return self.__callback(data)

        return data

    def beforeToJson(self, callback):
        self.__callback = callback

    def toJson(self, xxType = XX_TYPE_LIST, _file = None):
        data = self.toOriginData(xxType)
        jsonText = json.dumps(data, indent=4)
        if _file: write_file(_file, jsonText)

        return jsonText

def foreach_excelRows(excelPath, beginRowNum = 0, endRowNum = 0):
    wb = open_workbook(excelPath)
    for s in wb.sheets():
        for row in range(s.nrows):
            if(row.numerator < beginRowNum - 1):
                continue

            if(endRowNum != 0 and row.numerator >= endRowNum):
                break

            rowsValue = []
            flag = False
            for col in range(s.ncols):
                cell = s.cell(row,col)
                # print cell.ctype, cell.value
                if isinstance(cell.value, float) and cell.value == int(cell.value):
                    rowsValue.append(int(cell.value))
                    continue

                rowsValue.append(cell.value)
            yield rowsValue
    pass

def open_file(filePath, mode='w+', encoding='utf-8'):
    dirPath = os.path.dirname(filePath)
    if(dirPath and not os.path.exists(dirPath)):
        os.makedirs(dirPath)
    return open(filePath, mode=mode, encoding=encoding)

def write_file(filePath, text, encoding='utf-8'):
    f = open_file(filePath, 'w+', encoding)
    f.write(text)
    f.close()