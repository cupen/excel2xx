# encoding: utf-8
from typing import Optional
from collections import OrderedDict
import excel2xx.fields as fields

DEFINE_FIELDS = {
    "": fields.Auto,
    "auto": fields.Auto,
    "bool": fields.Bool,
    "int": fields.Int,
    "number": fields.Int,
    "float": fields.Float,
    "str": fields.String,
    "string": fields.String,
    "array": fields.Array,
    "array<int>": fields.IntArray,
    "array<float>": fields.FloatArray,
    "array<string>": fields.Array,
    "map<string,string>": fields.Map,
    "map<string, string>": fields.Map,
    "date": fields.Date,
    "datetime": fields.DateTime,
    "unixstamp": fields.UnixStamp,
    "object": fields.Object,
    "array<object>": fields.ObjectArray,
    "itemexpr": fields.ItemExpr,
    "array<itemexpr>": fields.ItemExprArray,
    "ItemExpr": fields.ItemExpr,
    "array<ItemExpr>": fields.ItemExprArray,
    "Reward": fields.Reward,
    "reward": fields.Reward,
    "Ratio": fields.Ratio,
    "ratio": fields.Ratio,
    "bignumber": fields.BigNumber,
    "BigNumber": fields.BigNumber,
    "json": fields.JSON,
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
        return self._lineNumCfg["name"]

    @property
    def typeRowIdx(self):
        return self._lineNumCfg["type"]

    @property
    def descRowIdx(self):
        return self._lineNumCfg["desc"]

    @property
    def dataRowIdx(self):
        return self._lineNumCfg["data"]

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
                raise RuntimeError(
                    '%-12s : Unexist field meta "%s". check the field(%s)'
                    % (excel.fname, fieldType, repr(typeRow[i]))
                )

            fields[fieldName] = fieldMeta(fieldName, fieldType, excel)
            i += 1
            pass
        return fields

    pass
