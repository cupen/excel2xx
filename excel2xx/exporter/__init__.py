# encoding: utf-8
from collections import OrderedDict
from excel2xx.fieldmeta import FieldMeta


def toKV(sheet, fields=("key", "type", "value")):
    d = OrderedDict()
    for row in sheet:
        key = row[fields[0]]
        valType = row[fields[1]]
        val = row[fields[2]]
        if isinstance(val, float):
            val = intIf(val)
            pass
        meta = FieldMeta.parseField(key, valType)
        if key in d:
            raise Exception(f"duplicated key: {key}")
        try:
            d[key] = meta.format(val)
        except Exception as ex:
            console.error(
                "%-12s : Field(name=%s type=%s). row: %s col: %s\n\t err: %s\n\t %s\n"
                % (
                    self.fname,
                    field.name,
                    field.type,
                    utils.show_row(rowNum),
                    utils.show_col(i),
                    str(ex),
                    cell.value,
                )
            )
            pass
        pass
    return d


def intIf(val):
    if isinstance(val, float):
        if val == float(int(val)):
            return int(val)
    return val
