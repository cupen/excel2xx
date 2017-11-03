# encoding: utf-8
from __future__ import unicode_literals, print_function
import os
import re
import xlrd
from collections import OrderedDict
from excel2xx import fields

__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'


class Excel:

    XX_TYPE_LIST = 1
    XX_TYPE_DICT = 2

    DEFINE_FIELDS = {
        '':       fields.Auto,
        'int':    fields.Int,
        'float':  fields.Float,
        'str':    fields.String,
        'string': fields.String,
        'array':  fields.Array,
        'date': fields.Date,
        'datetime': fields.DateTime,
    }

    def __init__(self, filePath, fieldRowNum=1):
        self.__filePath = filePath
        self.__fieldRowNum = fieldRowNum
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
    def fieldRowNum(self):
        return self.__fieldRowNum

    def getFieldRowNum(self):
        return self.__fieldRowNum

    def getSheet(self, sheetName, alias=''):
        sheet = None
        try:
            sheet = self.__wb.sheet_by_name(sheetName)
        except xlrd.XLRDError:
            sheet = self.__wb.sheet_by_name(alias)

        return Sheet(self, sheet)

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

    def getFieldMeta(self, fieldMetaName):
        return self.DEFINE_FIELDS.get(fieldMetaName)

    def setFieldMeta(self, fieldMetaName, field, overridable=False):
        if fieldMetaName in self.DEFINE_FIELDS and not overridable:
            raise RuntimeError('"%s" was existed.' % (fieldMetaName,))

        self.DEFINE_FIELDS[fieldMetaName] = field
        pass


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
        if len(self.__fields) > 0:
            return self.__fields.copy()

        fieldRowNum = self.__excel.fieldRowNum
        if self.__sheet.nrows < fieldRowNum:
            return {}

        fieldRowIndex = fieldRowNum - 1
        fieldRow = self.__sheet.row(fieldRowIndex)
        fields = OrderedDict()
        for cell in fieldRow:
            # print("cell.xf_index:%s ctype:%s" % (cell.xf_index, cell.ctype))
            tmpArr = list(map(lambda x: x.strip(), str(cell.value).split(':')))

            if len(tmpArr) not in (1, 2):
                raise RuntimeError('Invalid field(xf_index:%s ctype:%s value=%s' % (cell.xf_index, cell.ctype, cell.format))

            fieldName = tmpArr[0]
            fieldType = tmpArr[1] if len(tmpArr) == 2 else ''

            # print("fieldName={fieldName} fieldType={fieldType}".format(**locals()))
            fieldMeta = self.__excel.getFieldMeta(fieldType)
            if not fieldMeta:
                raise RuntimeError('Unexist field meta "%s". check the field value:=%s' % (fieldType, cell.format))

            fields[fieldName] = fieldMeta(fieldName, 0, self.__excel)

        self.__fields = fields
        return self.__fields

    def rows(self):
        skipRows = self.__excel.fieldRowNum
        for row in self.__sheet.get_rows():
            if skipRows > 0:
                skipRows -= 1
                continue

            yield row
        pass

    def getCellValue(self, cell):
        if isinstance(cell.format, float) and cell.format == int(cell.format):
            return int(cell.format)

        return cell.format

    def toList(self):
        return list(iter(self))

    def toDict(self):
        _dict = OrderedDict()
        firstField = None
        for row in self:
            if not row:
                continue

            if not firstField:
                for tmp in row.keys():
                    firstField = tmp
                    break
            _dict[row[firstField]] = row
        return _dict

    def toDataFrame(self):
        import pandas
        return pandas.DataFrame(self, columns=self.fields().keys())

    def __iter__(self):
        fields = self.fields()
        fieldsArr = tuple(fields.values())
        for row in self.rows():
            row = list(row)

            _dict = OrderedDict()
            for i in range(len(fieldsArr)):
                cell = row[i]
                field = fieldsArr[i]
                _dict[field.name] = field.format(cell.value)

            yield _dict
        pass
