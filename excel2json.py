# encoding:UTF-8
"""Export excel to json.

Usage:
    excel2json.py INPUT [--output=<output>] [--type=list]
    excel2json.py [options]

Arguments:
    INPUT    Excel file.

Options:
    --help show this help message and exit
    --version show version and exit
    -o --output=FILE output file
    -t --type=TYPE output json object type was 'list' or 'dict'. [default: list]


"""
__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'

import os
import re
import traceback
import json
import argparse
from collections import OrderedDict
from docopt import docopt
from xlrd import open_workbook

class Excel:

    def __init__(self, filePath, fieldRowNum = 2):
        # self.
        pass

    def toXX(self, xxType = 0):

        pass

    pass

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

def foreach_excelRowsMap(excelPath, beginRowNum = 0, endRowNum = 0, includes = None, excludes = None):
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
                if(not includes or includes.get(fieldName)):
                    rowDict[fieldName] = cell.value
                    if(not pattern.match(str(cell.value) if not isinstance(cell.value, str) else cell.value)):
                        flag = True
                else:
                    pass

        if(flag):
            # print(keyValueMap)
            yield rowDict
    pass

def open_file(filePath, mode='w+', encoding='utf-8'):
    dirPath = os.path.dirname(filePath)
    if(dirPath and not os.path.exists(dirPath)):
        os.makedirs(dirPath)
    return open(filePath, mode=mode, encoding=encoding)

def argsparsing():
    parser = argparse.ArgumentParser(
        description='Export Excel file to Lua code.',
        epilog="That's all!"
    )
    parser.add_argument('excelDirPath', nargs=1, help='The path of Excel directory.')
    parser.add_argument('--input', nargs=1, required=True, help='The path of Lua template files directory')
    parser.add_argument('--output', nargs=1, required=True, type=str, help='Export Lua code to this directory.')
    args = parser.parse_args()
    return args.excelDirPath[0].replace('\\','/'),\
           args.input[0].replace('\\','/'), \
           args.output[0].replace('\\','/')

def main(args):
    if args['--help']:
        print(__doc__)
        exit(0)

    excelFile = args.get('INPUT')
    jsonFile = args.get('--output')
    jsonType = args.get('--type')
    if not excelFile:
        print("Unexist 'INPUT'.")
        exit(1)

    if excelFile: excelFile = os.path.realpath(excelFile)
    if jsonFile: jsonFile = os.path.realpath(jsonFile)

    # print("Export '%s' to '%s'" % (excelFile, jsonFile))


    jsonObj = None
    if jsonType and jsonType == 'dict':
        jsonObj = OrderedDict()
        firstField = None
        for _dict in foreach_excelRowsMap(excelFile, 3):
            if not firstField:
                for tmp in _dict.keys():
                    firstField = tmp
                    break
            jsonObj[_dict[firstField]] = _dict
    else:
        jsonObj = []
        for _dict in foreach_excelRowsMap(excelFile, 3):
            jsonObj.append(_dict)

    jsonText = json.dumps(jsonObj, indent=4)
    if jsonFile:
        f = open_file(jsonFile)
        f.write(jsonText)
        f.close()
    else:
        print(jsonText)

    pass

if __name__ == '__main__':
    import sys
    # sys.argv += "example/test.xls --output test.js --type dict".split(' ')
    args = docopt(__doc__)
    main(args)
    pass
