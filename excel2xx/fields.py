# coding=utf-8
from __future__ import unicode_literals, print_function

import datetime
import re
import json
import math
from collections import namedtuple, OrderedDict
from pprint import pformat

from xlrd.xldate import xldate_as_datetime


class Field:
    def __init__(self, name, type, wb=None):
        self.name = name
        self.type = type
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
        pass

    pass


class Int(Field):
    def format(self, v):
        return int(v)


class Bool(Field):
    TRUE_VALUES = [1, 1.0, "true"]
    FALSE_VALUES = [0, 0.0, "false"]

    def format(self, v):
        # print(f"{type(v)}: {v}", end="")
        if v in self.TRUE_VALUES:
            return True
        if v in self.FALSE_VALUES:
            return False
        raise Exception(f"Invalid BoolValue: {type(v)}:({v})")
        pass


class String(Field):
    def format(self, v):
        v = str(v)
        v = v.replace("\\r\\n", "\n")
        v = v.replace("\\n", "\n")
        v = v.replace("\\r", "\n")
        return v


class Float(Field):
    """
    recommend using string, beacuse excel-float was'nt adhere IEEE 754.
    @see https://support.microsoft.com/en-us/help/78113/floating-point-arithmetic-may-give-inaccurate-results-in-excel
    """

    def format(self, v):
        return float(v)


class Array(Field):
    def format(self, v):
        if not v:
            return []
        _iter = map(lambda x: x.strip(), v.split(","))
        return list(_iter)


class IntArray(Field):
    def format(self, v):
        if not v:
            return []
        _iter = map(lambda x: x.strip(), v.split(","))
        return list(map(int, _iter))


class Ratio(Field):
    def format(self, v):
        try:
            if not v:
                raise Exception(f"empty value")
            arr = v.split(":")
            if len(arr) != 2:
                raise Exception("it must be two numbers.")
            _iter = map(lambda x: x.strip(), arr)
            return list(map(int, _iter))
        except Exception as ex:
            raise Exception(f"invalid Ratio: {v}. err:{ex}")


class FloatArray(Field):
    def format(self, v):
        if not v:
            return []
        _iter = map(lambda x: x.strip(), v.split(","))
        return list(map(float, _iter))


class Auto(Field):
    def format(self, v):
        return v


class Date2(Field):
    FORMAT = "%Y-%m-%d"

    def format(self, v):
        return datetime.datetime.strptime(v, self.FORMAT)


class DateTime2(Field):
    FORMAT = "%Y-%m-%dT%H:%M:%S%z"

    def format(self, v):
        return datetime.datetime.strptime(v, self.FORMAT)


class UnixStamp(DateTime2):
    def format(self, v):
        dt = super().format(v)
        return int(dt.timestamp() * 1000)


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


class Map(Field):
    def format(self, v: str) -> dict:
        rs = {}
        m = filter(lambda x: bool(x), v.split("\n"))
        for line in m:
            arr = line.split(":", maxsplit=1)
            if len(arr) != 2:
                raise Exception(f"Invalid map item {pformat(line)}")
            arr = list(map(lambda x: x.strip(), arr))
            rs[arr[0]] = arr[1]
        return rs


class Object(Field):
    Attr = namedtuple("Attr", ["name", "type"])

    def __init__(self, name, type, wb=None):
        super(Object, self).__init__(name, type, wb)
        self.attrs = self.parseType(text=type)
        pass

    def newException(self):
        return Exception(
            "Invalid object define. name:%s type:%s attrs:%s"
            % (self.name, self.type, self.attrs)
        )

    def parseType(self, text):
        text = text.strip()
        if not text.startswith("object"):
            raise self.newException()

        attrDefs = (
            text.replace("Object", "")
            .replace("object", "")
            .replace(" ", "")
            .strip("()")
            .split(",")
        )
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
                raise Exception(
                    'Warning: Invalid fieldType="%s" tmpArr=%s' % (text, tmpArr)
                )
                # print("Warning: Invalid fieldType %s" % text)
                name = tmpArr[0].strip()
                type = str

            attrs.append(self.Attr(name=name, type=type))
            pass
        return attrs

    def parseValue(self, attrs, valText):
        if not valText:
            return None
        vals = list(map(lambda x: x.strip(), valText.strip("{}<> ").split(",")))
        if len(vals) < len(self.attrs) - 1:
            attrs = ",".join(map(str, self.attrs))
            raise Exception(
                "Invalid object define. name:%s type:%s attrs:[%s] val:%s"
                % (self.name, self.type, attrs, valText)
            )

        d = OrderedDict()
        for i in range(len(vals)):
            attr = attrs[i]
            # if i >= len(vals):
            #     d[attr.name] = attr.type()
            #     continue
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
        return Exception(
            "Invalid array<object> define. name:%s type:%s attrs:%s"
            % (self.name, self.type, self.attrs)
        )

    def format(self, v):
        if not v:
            return []

        _list = []
        for tmpVal in self.pattern.findall(v):
            obj = super(ObjectArray, self).format(tmpVal.strip())
            _list.append(obj)
        return _list


class ItemExpr(Field):
    parseFuncs = {}

    @staticmethod
    def Default(arr):
        if len(arr) < 2 or len(arr) > 3:
            raise Exception(f"invalid itemexpr. {arr}")
        return {
            "type": arr[0],
            "id": arr[1],
            "count": int(arr[2]) if len(arr) >= 3 else 1,
        }

    @staticmethod
    def OnlyID(arr):
        if len(arr) < 2:
            raise Exception(f"invalid itemexpr-OnlyID. {arr}")
        if len(arr) >= 3 and arr[2] != "1":
            raise Exception(f"invalid itemexpr-OnlyID. {arr}")
        return {"type": arr[0], "id": arr[1], "count": 1}

    @staticmethod
    def OnlyCount(arr):
        if len(arr) != 2:
            raise Exception(f"invalid itemexpr-OnlyCount. {arr}")
        return {"type": arr[0], "count": int(arr[1])}

    @staticmethod
    def FloatCount(arr):
        if len(arr) != 2:
            raise Exception(f"invalid itemexpr-FloatCount. {arr}")
        return {"type": arr[0], "count": Number("", "").format(arr[1])}

    def __init__(self, name, type, wb=None):
        super(ItemExpr, self).__init__(name, type, wb)
        pass

    @classmethod
    def register(cls, name, parseFunc):
        if name in cls.parseFuncs:
            raise Exception(f"already registered. name:{name} parseFunc:{parseFunc}")
        cls.parseFuncs[name] = parseFunc
        pass

    @classmethod
    def setUnits(cls, units: str):
        units = units.strip(" \n\r,")
        units = "," + units

        idx = 0
        _dict = {}
        for v in map(lambda x: x.strip(), units.split(",")):
            _dict[v] = idx
            idx += 1
            pass
        cls.UNITS = _dict
        pass

    def newException(self, value):
        return Exception(
            "Invalid ItemExpr. name:%s type:%s value:%s" % (self.name, self.type, value)
        )

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
        parseFunc = self.parseFuncs.get(_type, ItemExpr.Default)
        return parseFunc(tmpArr)


class ItemExprArray(ItemExpr):
    def newException(self, value):
        return Exception(
            "Invalid Array<ItemExpr>. name:%s type:%s value:%s"
            % (self.name, self.type, value)
        )

    def format(self, v):
        if not isinstance(v, str):
            raise self.newException(v)

        if not v:
            return []
        _iter = map(lambda x: x.strip(), v.split(","))
        _iter = map(lambda x: super(ItemExprArray, self).format(x), _iter)
        return list(_iter)


class Reward(ItemExpr):
    def newException(self, value):
        return Exception(
            "Invalid Array<ItemExpr>. name:%s type:%s value:%s"
            % (self.name, self.type, value)
        )

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
        if not v:
            return []
        if not isinstance(v, str):
            raise self.newException(v)

        _iter = map(lambda x: x.strip(), v.split(";"))
        _iter = map(lambda x: self.parseItemExprWithWeight(x), _iter)
        return list(_iter)


class Number(Field):
    """
    Float64

    >>> n = Number("test", type="number")
    >>> n.format("1K")
    1024.0
    >>> n.format("1.2K")
    1228.8
    >>> n.format("512.1048576M")
    536980863.1627775
    """

    UNITS = {}
    UNITS_IDX = {}
    PARTERN = re.compile(r"(?P<count>\d+\.?\d*)(?P<unit>[a-zA-Z_]*)")

    def newException(self, value, suffix=""):
        return Exception(
            "Invalid BigNumber. name:%s type:%s value:%s. suffix:%s"
            % (self.name, self.type, value, suffix)
        )

    @classmethod
    def setUnits(cls, units, size=1000):
        units = units.strip(" \n\r,")
        if isinstance(units, str):
            units = map(lambda x: x.strip(), units.split(","))

        idx = 0
        _dict = {}
        _dict2 = {}
        for v in units:
            idx += 1
            _dict[v] = idx - 1
            _dict2[v] = math.pow(size, idx)
            pass

        cls.UNITS_IDX = _dict
        cls.UNITS = _dict2
        pass

    def format(self, v):
        if isinstance(v, float):
            return v

        if not v or not isinstance(v, str):
            raise self.newException(v)

        _dict = self.PARTERN.match(v).groupdict()
        if "count" not in _dict:
            raise self.newException(v)
        if "unit" not in _dict:
            raise self.newException(v)
        if _dict["unit"] and _dict["unit"] not in self.UNITS:
            raise self.newException(v, suffix=f"Invalid UNITS {self.UNITS}")
        unit = 1
        if _dict["unit"] != "":
            unit = self.UNITS[_dict["unit"]]
        count = float(_dict["count"])
        return count * unit


Number.setUnits("K,M,G,T,P,E", size=1024)
BigNumber = Number


class JSON(ItemExpr):
    def newException(self, value):
        return Exception(
            "invalid json. name:%s type:%s value:%s" % (self.name, self.type, value)
        )

    def parseJson(self, value):
        return json.loads(value)

    def format(self, v):
        if not v:
            return None
        if not isinstance(v, str):
            raise self.newException(v)
        return self.parseJson(v)
