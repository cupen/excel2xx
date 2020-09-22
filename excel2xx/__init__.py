# encoding: utf-8
from __future__ import unicode_literals, print_function
import os
import re
import types

import xlrd
from collections import OrderedDict
from excel2xx import fields, utils
from typing import Optional

__author__ = 'cupen'
__email__ = 'xcupen@gmail.com'

DEFINE_FIELDS = {
    '':       fields.Auto,
    'auto':   fields.Auto,

    'bool':    fields.Bool,
    'int':    fields.Int,
    'number': fields.Int,
    'float':  fields.Float,
    'str':    fields.String,
    'string': fields.String,

    'array':  fields.Array,
    'array<int>': fields.IntArray,
    'array<float>': fields.FloatArray,
    'array<string>': fields.Array,

    'map<string,string>': fields.Map,
    'map<string, string>': fields.Map,

    'date': fields.Date,
    'datetime': fields.DateTime,
    'unixstamp': fields.UnixStamp,

    'object': fields.Object,
    'array<object>': fields.ObjectArray,

    'itemexpr': fields.ItemExpr,
    'array<itemexpr>': fields.ItemExprArray,

    'ItemExpr': fields.ItemExpr,
    'array<ItemExpr>': fields.ItemExprArray,

    'Reward': fields.Reward,
    'reward': fields.Reward,

    'bignumber': fields.BigNumber,
    'BigNumber': fields.BigNumber,
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

    @classmethod
    def parseFieldType(cls, fieldType: str) -> str:
        fieldType = fieldType.replace(" ", "")
        if fieldType.startswith("object") or fieldType.startswith("Object"):
            return "object"

        if fieldType.startswith("array<object") or fieldType.startswith("array<Object"):
            return "array<object>"
        return fieldType

    @classmethod
    def parseField(cls, name: str, fieldType: str) -> Optional[fields.Field]:
        name = cls.parseFieldType(fieldType)
        meta = DEFINE_FIELDS.get(name)
        if not meta:
            return None
        return meta(name, fieldType)


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

            if not fieldName or fieldName.startswith("#"):
                continue
            fieldMeta = DEFINE_FIELDS.get(self.parseFieldType(fieldType))
            if not fieldMeta:
                raise RuntimeError('%-12s : Unexist field meta "%s". check the field(%s)' % (excel.fname, fieldType, repr(typeRow[i])))

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

    @property
    def fname(self):
        if isinstance(self.__filePath, str):
            return os.path.basename(self.__filePath)

        with open("/dev/null") as f:
            fileType = type(f)
            if isinstance(self.__filePath, fileType):
                return self.__filePath.name

        return ""

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
        for fieldName in fields:
            return fieldName
        return None

    def throwException(self, text):
        raise Exception(f"Sheet(name={self.name}): {text}")

    def toDict(self, valueIsList=False):
        _dict = OrderedDict()
        firstField = self.firstFieldName()
        if not firstField:
            return self.throwException(f"Invalid first field name. \"{firstField}\"")
        for row in self:
            if not row:
                continue

            value = row[firstField]
            if (not valueIsList) and (value in _dict):
                return self.throwException("Duplicate value of field name. %s=%s" % (firstField, value))
            _dict[value] = row
        return _dict

    def toDict2(self):
        _dict = OrderedDict()
        firstField = self.firstFieldName()
        if not firstField:
            return self.throwException("Invalid first field name. %s" % firstField)
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

    @property
    def fname(self):
        return self.__excel.fname

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
                    print("%-12s : Failed to parse the value:\"%s\" of Field(name=%s type=%s). row: %s col: %s\n\t err: %s" \
                          %(self.fname,  cell.value, field.name, field.type, utils.show_row(rowNum), utils.show_col(i), str(ex)))
                    pass

            yield _dict
        pass


def addFieldType(typeName, parser):
    DEFINE_FIELDS[typeName] = parser
    pass


def delFieldType(typeName, parser):
    del DEFINE_FIELDS[typeName]
    pass

def setUnits(text, size=1000):
    fields.BigNumber.setUnits(text, size=size)
    fields.ItemExpr.setUnits(text)
    fields.ItemExpr.addNoIdType("coin", "coin-(?P<count__int>\d+)(?P<unit>[a-zA-Z_]*)")
    pass
