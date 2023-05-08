# coding: utf-8
from __future__ import unicode_literals, print_function
import sys
import json
from collections import OrderedDict
from pprint import pformat
from mako.template import Template
from io import open
from datetime import datetime, date


def _defaultSerialize(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def toJson(excel, output, encoding="utf-8"):
    _dict = OrderedDict()
    for sheet in excel:
        _dict[sheet.name] = list(sheet)

    if sys.version_info[0] == 2:
        with open(output, mode="wb") as f:
            json.dump(
                _dict,
                f,
                ensure_ascii=False,
                encoding=encoding,
                default=_defaultSerialize,
            )
        return

    with open(output, mode="w", encoding=encoding) as f:
        json.dump(_dict, f, ensure_ascii=False, indent=4, default=_defaultSerialize)
    pass


def toMako(excel, output, template, encoding="utf-8"):
    with open(output, mode="w", encoding=encoding) as ouputfile:
        text = ""
        with open(template, mode="r", encoding=encoding) as f:
            text = Template(f.read()).render(excel=excel, format=pformat)
        ouputfile.write(text)
    pass


def toMsgPack(excel, output, encoding="utf-8"):
    import msgpack

    _dict = OrderedDict()
    for sheet in excel:
        _dict[sheet.name] = list(sheet)

    with open(output, mode="wb") as f:
        f.write(msgpack.packb(_dict, default=_defaultSerialize))
    pass
