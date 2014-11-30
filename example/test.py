__author__ = 'cupen'

from excel2xx import Excel, write_file

excelFile = 'test.xls'
excel = Excel(excelFile)

# 直接导出为json
excel.toJson(Excel.XX_TYPE_DICT, excelFile+".json")

# 导出为list json结构,并拼凑出代码
jsonText = "const test = {test}\n".format(test=excel.toJson(Excel.XX_TYPE_LIST))
write_file(excelFile + '.list.js', jsonText)

# 导出为dict json结构,并拼凑出代码
jsonText = "const test = {test}\n".format(test=excel.toJson(Excel.XX_TYPE_DICT))
write_file(excelFile + '.dict.js', jsonText)

# 预处理一遍再导出为json,并拼凑出代码
def _callback(data):
    data['a'] = 1
    data['b'] = 2
    data['c'] = 3
    data['d'] = 4
    return data

excel.beforeToJson(_callback)
jsonText = "const test = {test}\n".format(test=excel.toJson(Excel.XX_TYPE_DICT))
write_file(excelFile + '.dict.pre.js', jsonText)
