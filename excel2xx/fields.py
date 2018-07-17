# coding:utf-8
from __future__ import unicode_literals, print_function

from collections import namedtuple, OrderedDict

from xlrd.xldate import xldate_as_datetime

__author__ = 'cupen'
__email__ = 'xcupen@gmail.com'

class Field:
    def __init__(self, name, type, wb=None):
        self.name = name
        self.type= type
        self.wb = wb
        pass

    def format(self, v):
        raise NotImplementedError

    def as_type(self, typeName):
        typeName = typeName.strip()
        if typeName == "int":
            return int
        if typeName == "string":
            return str
        if typeName == "float":
            return float
        raise Exception("Invalid type %s" % typeName)


class Int(Field):
    def format(self, v):
        return int(v)


class String(Field):
    def format(self, v):
        return str(v)


class Float(Field):
    def format(self, v):
        return float(v)


class Array(Field):
    def format(self, v):
        _iter = map(lambda x: x.strip(), v.split(","))
        return list(_iter)


class IntArray(Field):
    def format(self, v):
        _iter = map(lambda x: x.strip(), v.split(","))
        return list(map(int, _iter))


class Auto(Field):
    def format(self, v):
        return v


class Date(Field):
    def format(self, v):
        try:
            return xldate_as_datetime(v, self.wb.datemode).date()
        except:
            return None


class DateTime(Field):
    def format(self, v):
        try:
            return xldate_as_datetime(v, self.wb.datemode)
        except:
            return None


class Object(Field):
    def __init__(self, name, type, wb=None):
        super(Object, self).__init__(name, type, wb)
        self.attrs = self.parseValue(text=type)
        pass

    def newException(self):
        return Exception("Invalid object define. name:%s type:%s attrs:%s" % (self.name, self.type, self.attrs))

    def parseValue(self, text):
        text = text.strip()
        if not text.startswith("object"):
            raise self.newException()
        attrDefs = text.replace("object", "").replace(" ", "").strip("()").split(",")
        if len(attrDefs) <= 0:
            raise self.newException()

        attrs = []
        for attrDefine in attrDefs:
            tmpArr = attrDefine.split(":")
            attr = namedtuple("Attr", ["name", "type"])
            if len(tmpArr) == 1:
                attr.name = tmpArr[0].strip()
                attr.type = str
            if len(tmpArr) >= 2:
                attr.name = tmpArr[0].strip()
                attr.type = self.as_type(tmpArr[1])
            attrs.append(attr)
            pass
        return attrs

    def format(self, v):
        vals = list(map(lambda x: x.strip(), v.strip("{}<> ").split(",")))
        if len(vals) != len(self.attrs):
            raise Exception("Invalid object define. name:%s type:%s attrs:%s val:%s" % (self.name, self.type, self.attrs, v))

        d = OrderedDict()
        for i in range(0, len(vals)):
            attr = self.attrs[i]
            d[attr.name] = attr.type(vals[i])
            pass
        return d


class ItemExpr(Field):
    def __init__(self, name, type, wb=None):
        super(ItemExpr, self).__init__(name, type, wb)
        pass

    def newException(self, value):
        return Exception("Invalid ItemExpr. name:%s type:%s value:%s" % (self.name, self.type, value))

    def format(self, v):
        if not isinstance(v, (str, list)):
            raise self.newException(v)

        tmpArr = v
        if isinstance(tmpArr, str):
            tmpArr = v.split("-")

        if len(tmpArr) <= 0:
            raise self.newException(v)

        _type = tmpArr[0]
        _id = "" if len(tmpArr) == 2 else tmpArr[1]
        count = int(tmpArr[2]) if len(tmpArr) >= 3 else int(tmpArr[1])

        rs =  {
            "type": _type,
            "id": _id,
            "count": count
        }
        if not rs["id"]:
            del rs["id"]
        return rs


class ItemExprArray(ItemExpr):
    def newException(self, value):
        return Exception("Invalid Array<ItemExpr>. name:%s type:%s value:%s" % (self.name, self.type, value))

    def format(self, v):
        if not isinstance(v, str):
            raise self.newException(v)

        _iter = map(lambda x: x.strip(), v.split(","))
        _iter = map(lambda x: super(ItemExprArray, self).format(x), _iter)
        return list(_iter)


class Reward(ItemExpr):
    def newException(self, value):
        return Exception("Invalid Array<ItemExpr>. name:%s type:%s value:%s" % (self.name, self.type, value))

    def parseItemExprWithWeight(self, expr_w):
        tmpArr = expr_w.split(",")
        weight = int(tmpArr[0])
        if len(tmpArr) < 2:
            raise self.newException(expr_w)

        exprObj = ItemExpr.format(self, tmpArr[1])
        return {
            "weight": weight,
            "item": exprObj,
        }

    def format(self, v):
        if not isinstance(v, str):
            raise self.newException(v)

        _iter = map(lambda x: x.strip(), v.split(";"))
        _iter = map(lambda x: self.parseItemExprWithWeight(x), _iter)
        return list(_iter)