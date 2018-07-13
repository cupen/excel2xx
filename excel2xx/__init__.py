# encoding: utf-8
from __future__ import unicode_literals, print_function
import os
import re
import xlrd
from collections import OrderedDict
from excel2xx import fields

__author__ = 'cupen'
__email__ = 'xcupen@gmail.com'

DEFINE_FIELDS = {
    '':       fields.Auto,
    'auto':   fields.Auto,

    'int':    fields.Int,
    'number': fields.Int,
    'float':  fields.Float,
    'str':    fields.String,
    'string': fields.String,

    'array':  fields.Array,
    'array<int>': fields.IntArray,
    'array<string>': fields.Array,

    'date': fields.Date,
    'datetime': fields.DateTime,

    'object': fields.Object,
    'itemexpr': fields.ItemExpr,
    'array<itemexpr>': fields.ItemExprArray,

    'Object': fields.Object,
    'ItemExpr': fields.ItemExpr,
    'array<ItemExpr>': fields.ItemExprArray,
    'Reward': fields.Reward,
}


class FieldMeta:
    def __init__(self, name=0, type=1, desc=2, data=3):
        self._lineNumCfg = {
            "name": name,
            "type": type,
            "desc": desc,
            "data": data,
        }
        pass

    @property
    def nameRowIdx(self):
        return self._lineNumCfg['name']

    @property
    def typeRowIdx(self):
        return self._lineNumCfg['type']

    @property
    def descRowIdx(self):
        return self._lineNumCfg['desc']

    @property
    def dataRowIdx(self):
        return self._lineNumCfg['data']

    def parseFieldType(self, fieldType):
        if fieldType.startswith("object"):
            return "object"
        return fieldType

    def parseSheet(self, excel, sheet):
        if sheet.nrows < self.nameRowIdx + 1:
            return {}

        nameRow = sheet.row(self.nameRowIdx)
        typeRow = sheet.row(self.typeRowIdx)
        # descRow = sheet.row(self.descRowIdx)

        fields = OrderedDict()
        for i in range(0, len(nameRow)):
            fieldName = str(nameRow[i].value).strip()
            fieldType = str(typeRow[i].value).strip()

            fieldMeta = DEFINE_FIELDS.get(self.parseFieldType(fieldType))
            if not fieldMeta:
                raise RuntimeError('Unexist field meta "%s". check the field(%s)' % (fieldType, repr(typeRow[i])))

            fields[fieldName] = fieldMeta(fieldName, fieldType, excel)
            i += 1
            pass
        return fields
    pass

class Excel:
    def __init__(self, fpathOrFp, fieldMeta=FieldMeta(name=0, type=1, desc=2, data=3)):
        self.__filePath = fpathOrFp
        self.fieldMeta = fieldMeta

        self.__callback = None
        if isinstance(self.__filePath, str):
            self.__wb = xlrd.open_workbook(self.__filePath)
        else:
            self.__wb = xlrd.open_workbook(file_contents=self.__filePath.read())
        pass

    @property
    def datemode(self):
        return self.__wb.datemode

    def getSheet(self, sheetName, alias=''):
        sheet = None
        try:
            sheet = self.__wb.sheet_by_name(sheetName)
        except xlrd.XLRDError as e:
            if not alias:
                raise e
            sheet = self.__wb.sheet_by_name(alias)
        return Sheet(self, sheet)

    def __getitem__(self, nameOrIdx):
        if isinstance(nameOrIdx, int):
            sheet = self.__wb.sheet_by_index(nameOrIdx)
            return Sheet(self, sheet)
        return self.getSheet(nameOrIdx)

    def __iter__(self):
        sheets = map(lambda x: Sheet(self, x), self.__wb.sheets())
        for sheet in sheets:
            if sheet.name.startswith('#'):
                continue
            # sheet.name
            yield sheet
        pass

    def toList(self):
        _dict = OrderedDict()
        for sheet in self:
            _dict[sheet.name] = sheet.toList()
        return _dict

    def toDict(self):
        _dict = OrderedDict()
        for sheet in self:
            _dict[sheet.name] = sheet.toDict()
        return _dict


class Sheet:

    def __init__(self, excel, sheet):
        self.__excel = excel
        self.__sheet = sheet
        self.__fields = {}
        pass

    @property
    def name(self):
        return self.__sheet.name

    def fields(self):
        """
        :rtype: dict of [str, Field]
        """
        sheet = self.__sheet
        # fieldMeta = self.__excel.fieldMeta
        if len(self.__fields) <= 0:
            self.__fields = self.__excel.fieldMeta.parseSheet(self.__excel, sheet)
        return self.__fields.copy()

    def rows(self):
        skipRows = self.__excel.fieldMeta.dataRowIdx
        for row in self.__sheet.get_rows():
            if skipRows > 0:
                skipRows -= 1
                # print(row)
                continue

            yield row
        pass

    def toList(self):
        return list(iter(self))

    def firstFieldName(self):
        fields = self.fields()
        for fieldName  in fields:
            return fieldName
        return None

    def toDict(self, valueIsList=False):
        _dict = OrderedDict()
        firstField = self.firstFieldName()
        if not firstField:
            raise Exception("Invalid first field name. %s" % firstField)
        for row in self:
            if not row:
                continue

            value = row[firstField]
            if (not valueIsList) and (value in _dict):
                raise Exception("Duplicate value of field name. %s=%s" % (firstField, value))
            _dict[value] = row
        return _dict

    def toDict2(self):
        _dict = OrderedDict()
        firstField = self.firstFieldName()
        if not firstField:
            raise Exception("Invalid first field name. %s" % firstField)
        for row in self:
            if not row:
                continue

            value = row[firstField]
            if value not in _dict:
                _dict[value] = []
            _dict[value].append(row)
        return _dict

    def toDataFrame(self):
        import pandas
        return pandas.DataFrame(self, columns=self.fields().keys())

    def __iter__(self):
        fields = self.fields()
        fieldsArr = tuple(fields.values())
        rowNum = 0
        for row in self.rows():
            rowNum += 1
            row = list(row)

            _dict = OrderedDict()
            for i in range(len(fieldsArr)):
                cell = row[i]
                field = fieldsArr[i]
                try:
                    _dict[field.name] = field.format(cell.value)
                except Exception as ex:
                    print("Failed to parse the value(\"%s\") of Field(%s). row: %s col: %s" %(cell.value, field.type, rowNum, i))
                    pass

            yield _dict
        pass


def addFieldType(typeName, parser):
    DEFINE_FIELDS[typeName] = parser
    pass


def delFieldType(typeName, parser):
    del DEFINE_FIELDS[typeName]
    pass