# coding:utf-8
from __future__ import unicode_literals, print_function

import re
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

    @classmethod
    def as_type(cls, typeName):
        typeName = typeName.strip()
        if typeName == "int":
            return int
        if typeName == "string":
            return str
        if typeName == "float":
            return float
        if typeName == "ItemExpr":
            return ItemExpr("as_type", typeName).format
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


class FloatArray(Field):
    def format(self, v):
        _iter = map(lambda x: x.strip(), v.split(","))
        return list(map(float, _iter))


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
    Attr = namedtuple("Attr", ["name", "type"])
    def __init__(self, name, type, wb=None):
        super(Object, self).__init__(name, type, wb)
        self.attrs = self.parseType(text=type)
        pass

    def newException(self):
        return Exception("Invalid object define. name:%s type:%s attrs:%s" % (self.name, self.type, self.attrs))

    def parseType(self, text):
        text = text.strip()
        if not text.startswith("object"):
            raise self.newException()

        attrDefs = text.replace("Object", "").replace("object", "").replace(" ", "").strip("()").split(",")
        if len(attrDefs) <= 0:
            raise self.newException()

        attrs = []
        for attrDefine in attrDefs:
            tmpArr = attrDefine.split(":")
            if len(tmpArr) == 1:
                name = tmpArr[0].strip()
                type = str
            elif len(tmpArr) >= 2:
                name = tmpArr[0].strip()
                type = self.as_type(tmpArr[1])
            else:
                raise Exception("Warning: Invalid fieldType=\"%s\" tmpArr=%s" % (text, tmpArr))
                # print("Warning: Invalid fieldType %s" % text)
                name = tmpArr[0].strip()
                type = str

            attrs.append(self.Attr(name=name, type=type))
            pass
        return attrs

    def parseValue(self, attrs, valText):
        vals = list(map(lambda x: x.strip(), valText.strip("{}<> ").split(",")))
        if len(vals) != len(self.attrs):
            attrs = ",".join(map(str, self.attrs))

            raise Exception(
                "Invalid object define. name:%s type:%s attrs:[%s] val:%s" % (self.name, self.type, attrs, valText))

        d = OrderedDict()
        for i in range(0, len(vals)):
            attr = attrs[i]
            d[attr.name] = attr.type(vals[i])
            pass
        return d

    def format(self, v):
        return self.parseValue(self.attrs, v)


class ObjectArray(Object):
    pattern = re.compile("{[^{^}]*}")

    def __init__(self, name, type, wb=None):
        _type = type.replace("array", "").strip("<>")
        super(ObjectArray, self).__init__(name, _type, wb=wb)
        pass

    def newException(self):
        return Exception("Invalid array<object> define. name:%s type:%s attrs:%s" % (self.name, self.type, self.attrs))

    def format(self, v):
        _list = []
        for tmpVal in self.pattern.findall(v):
            obj = super(ObjectArray, self).format(tmpVal.strip())
            _list.append(obj)
        return _list

class ItemExpr(Field):
    NO_ID = set()
    NO_ID_PATTERN = {
        "coin": re.compile("coin-(?P<count__int>\d+)(?P<unit>[a-zA-Z_]*)")
    }

    def __init__(self, name, type, wb=None):
        super(ItemExpr, self).__init__(name, type, wb)
        pass

    @classmethod
    def addNoIdType(cls, typeNmae, pattern=""):
        cls.NO_ID.add(typeNmae)
        if pattern: cls.NO_ID_PATTERN[typeNmae] = re.compile(pattern)
        pass

    def newException(self, value):
        return Exception("Invalid ItemExpr. name:%s type:%s value:%s" % (self.name, self.type, value))

    def format(self, v):
        if not isinstance(v, (str, list)):
            raise self.newException(v)

        if v == "":
            return None

        tmpArr = v
        if isinstance(tmpArr, str):
            tmpArr = v.split("-")

        if len(tmpArr) <= 0:
            raise self.newException(v)

        _type = tmpArr[0]
        if _type in self.NO_ID:
            ptn = self.NO_ID_PATTERN.get(_type)
            if not ptn:
                return {
                    "type": _type,
                    "count": int(tmpArr[1]),
                }
                pass

            _dict = ptn.match(v).groupdict()
            for k, v in dict(_dict).items():
                if "__" in k:
                    newk, t = k.split("__", 2)
                    _dict[newk] = self.as_type(t)(v)
                    del _dict[k]
                pass

            _dict["type"] = _type
            return _dict

        return {
            "type": _type,
            "id": tmpArr[1],
            "count": int(tmpArr[2]) if len(tmpArr) >= 3 else 1
        }


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